from __future__ import annotations

import re
from typing import Dict, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QGridLayout,
    QWidget,
)

from ui.styles.theme import (
    BORDER,
    PRIMARY_COLOR,
    SURFACE,
    TEXT_DARK,
    TEXT_MUTED,
)


class HeatmapPage(QWidget):
    def __init__(self):
        super().__init__()
        self.feature_names = [f"x{i}" for i in range(1, 21)]
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {SURFACE};
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        self.setLayout(layout)

        title = QLabel("Feature Heatmap")
        title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 26px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }}
        """)

        description = QLabel(
            "The matrix visualizes the contributions of transformed predictors "
            "to the model decision. Green cells increase the likelihood of class 1, "
            "while red cells decrease it."
        )
        description.setWordWrap(True)
        description.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 15px;
                background-color: transparent;
                border: none;
            }}
        """)

        self.empty_state = self._create_empty_state()

        self.heatmap_card = QFrame()
        self.heatmap_card.setMinimumHeight(700)
        self.heatmap_card.setStyleSheet(f"""
            QFrame {{
                background-color: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 16px;
            }}
        """)
        self.heatmap_card.hide()

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)
        self.heatmap_card.setLayout(card_layout)

        self.legend = QLabel(
            "Red: negative contribution | White: neutral | Green: positive contribution"
        )
        self.legend.setAlignment(Qt.AlignCenter)
        self.legend.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 13px;
                padding: 8px;
                background-color: transparent;
                border: none;
            }}
        """)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(False)
        self.scroll.setMinimumHeight(620)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)

        self.container = QWidget()
        self.container.setMinimumSize(1900, 1100)
        self.container.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)

        self.grid = QGridLayout()
        self.grid.setSpacing(4)
        self.grid.setContentsMargins(16, 16, 16, 16)
        self.container.setLayout(self.grid)

        self.scroll.setWidget(self.container)

        card_layout.addWidget(self.legend)
        card_layout.addWidget(self.scroll)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.empty_state)
        layout.addWidget(self.heatmap_card)
        layout.addStretch()

    def _create_empty_state(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 16px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)
        card.setLayout(layout)

        icon = QLabel("▦")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet(f"""
            QLabel {{
                color: {PRIMARY_COLOR};
                font-size: 46px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }}
        """)

        title = QLabel("No heatmap generated yet")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 20px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }}
        """)

        text = QLabel(
            "Run the analysis to generate a feature contribution matrix.\n\n"
            "The heatmap will show how transformed predictors influence "
            "the final classification decision."
        )
        text.setAlignment(Qt.AlignCenter)
        text.setWordWrap(True)
        text.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 14px;
                background-color: transparent;
                border: none;
            }}
        """)

        hint = QLabel("Go to Upload Data to build the heatmap.")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"""
            QLabel {{
                color: {PRIMARY_COLOR};
                font-size: 14px;
                font-weight: 600;
                background-color: transparent;
                border: none;
            }}
        """)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(text)
        layout.addWidget(hint)

        return card

    def _clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _parse_expression(self, expression: str) -> Tuple[str, str] | None:
        expression = expression.strip()

        binary_match = re.fullmatch(r"(x\d+)\s*([\*/])\s*(x\d+)", expression)
        if binary_match:
            left, operator, right = binary_match.groups()
            return left, right

        power_match = re.fullmatch(r"(x\d+)\^2", expression)
        if power_match:
            feature = power_match.group(1)
            return feature, feature

        single_match = re.fullmatch(r"x\d+", expression)
        if single_match:
            return expression, expression

        return None

    def _build_matrix(self, contributions: Dict[str, float]) -> Dict[Tuple[str, str], float]:
        matrix = {}

        for expression, contribution in contributions.items():
            parsed = self._parse_expression(expression)

            if not parsed:
                continue

            row_feature, col_feature = parsed

            if row_feature not in self.feature_names or col_feature not in self.feature_names:
                continue

            matrix[(row_feature, col_feature)] = contribution

            if "*" in expression:
                matrix[(col_feature, row_feature)] = contribution

        return matrix

    def _color_for_value(self, value: float, max_abs: float) -> str:
        if abs(value) < 1e-12 or max_abs == 0:
            return "rgb(248, 248, 248)"

        intensity = min(abs(value) / max_abs, 1.0)

        if value > 0:
            red = int(248 - 90 * intensity)
            green = int(248 - 35 * intensity)
            blue = int(248 - 90 * intensity)
        else:
            red = int(248)
            green = int(248 - 105 * intensity)
            blue = int(248 - 105 * intensity)

        return f"rgb({red}, {green}, {blue})"

    def _cell_style(self, background: str, bold: bool = False) -> str:
        weight = "bold" if bold else "normal"

        return f"""
            QLabel {{
                background-color: {background};
                color: #1F1F1F;
                border: 1px solid #DDE6DC;
                border-radius: 8px;
                padding: 4px;
                font-size: 13px;
                font-weight: {weight};
            }}
        """

    def _make_cell(self, text: str, background: str, bold: bool = False) -> QLabel:
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setFixedSize(82, 46)
        label.setStyleSheet(self._cell_style(background, bold))
        return label

    def show_heatmap(self, result: dict):
        self._clear_grid()

        contributions = result["prediction"]["feature_contributions"]
        matrix = self._build_matrix(contributions)

        if not matrix:
            self.empty_state.show()
            self.heatmap_card.hide()
            return

        max_abs = max(abs(value) for value in matrix.values())

        self.grid.addWidget(self._make_cell("", "#FFFFFF", True), 0, 0)

        for col, feature_name in enumerate(self.feature_names, start=1):
            self.grid.addWidget(
                self._make_cell(feature_name, "#F1F4F0", True),
                0,
                col,
            )

        for row, row_feature in enumerate(self.feature_names, start=1):
            self.grid.addWidget(
                self._make_cell(row_feature, "#F1F4F0", True),
                row,
                0,
            )

            for col, col_feature in enumerate(self.feature_names, start=1):
                value = matrix.get((row_feature, col_feature), 0.0)
                background = self._color_for_value(value, max_abs)

                text = "—" if abs(value) < 1e-12 else f"{value:.2f}"

                self.grid.addWidget(
                    self._make_cell(text, background),
                    row,
                    col,
                )

        self.empty_state.hide()
        self.heatmap_card.show()