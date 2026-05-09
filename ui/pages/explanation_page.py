from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ui.styles.theme import (
    BORDER,
    PRIMARY_COLOR,
    SURFACE,
    TEXT_DARK,
    TEXT_MUTED,
    text_box_style,
)
from ui.widgets.feature_table import FeatureTable


class ExplanationPage(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        self.setLayout(layout)

        title = QLabel("Model Decision Explanation")
        title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 26px;
                font-weight: bold;
            }}
        """)

        description = QLabel(
            "This page explains which transformed predictors had the strongest influence "
            "on the logistic regression decision."
        )
        description.setWordWrap(True)
        description.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 15px;
            }}
        """)

        self.empty_state = self._create_empty_state()

        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)
        self.summary_box.setStyleSheet(text_box_style())
        self.summary_box.setMaximumHeight(140)
        self.summary_box.hide()

        self.positive_label = QLabel("Top Positive Contributions")
        self.positive_label.setStyleSheet(self._section_label_style())
        self.positive_label.hide()

        self.positive_table = FeatureTable()
        self.positive_table.hide()

        self.negative_label = QLabel("Top Negative Contributions")
        self.negative_label.setStyleSheet(self._section_label_style())
        self.negative_label.hide()

        self.negative_table = FeatureTable()
        self.negative_table.hide()

        self.absolute_label = QLabel("Top Contributions by Absolute Value")
        self.absolute_label.setStyleSheet(self._section_label_style())
        self.absolute_label.hide()

        self.absolute_table = FeatureTable()
        self.absolute_table.hide()

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.empty_state)

        layout.addWidget(self.summary_box)

        layout.addWidget(self.positive_label)
        layout.addWidget(self.positive_table)

        layout.addWidget(self.negative_label)
        layout.addWidget(self.negative_table)

        layout.addWidget(self.absolute_label)
        layout.addWidget(self.absolute_table)

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

        icon = QLabel("🧠")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("""
            QLabel {
                font-size: 42px;
                border: none;
            }
        """)

        title = QLabel("No explanation available yet")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 20px;
                font-weight: bold;
                border: none;
            }}
        """)

        text = QLabel(
            "Run the analysis to identify which predictors increased or decreased "
            "the final model score.\n\n"
            "The explanation will include:\n"
            "• positive contributions\n"
            "• negative contributions\n"
            "• strongest predictors by absolute value"
        )
        text.setAlignment(Qt.AlignCenter)
        text.setWordWrap(True)
        text.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 14px;
                border: none;
            }}
        """)

        hint = QLabel("Go to Upload Data to generate an explanation.")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"""
            QLabel {{
                color: {PRIMARY_COLOR};
                font-size: 14px;
                font-weight: 600;
                border: none;
            }}
        """)

        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(text)
        layout.addWidget(hint)

        return card

    def _section_label_style(self) -> str:
        return f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 18px;
                font-weight: bold;
            }}
        """

    def _set_content_visible(self, visible: bool):
        self.summary_box.setVisible(visible)

        self.positive_label.setVisible(visible)
        self.positive_table.setVisible(visible)

        self.negative_label.setVisible(visible)
        self.negative_table.setVisible(visible)

        self.absolute_label.setVisible(visible)
        self.absolute_table.setVisible(visible)

    def show_explanation(self, result: dict):
        explanation = result["explanation"]

        self.empty_state.hide()
        self._set_content_visible(True)

        self.summary_box.setText(explanation["summary"])

        self.positive_table.set_contributions(
            explanation["top_positive_contributions"],
            "Positive"
        )

        self.negative_table.set_contributions(
            explanation["top_negative_contributions"],
            "Negative"
        )

        self.absolute_table.set_contributions(
            explanation["top_absolute_contributions"],
            "Absolute"
        )