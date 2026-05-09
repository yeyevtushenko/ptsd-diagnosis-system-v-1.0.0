from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.styles.theme import BORDER, SURFACE, TEXT_DARK


class FeatureTable(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Feature", "Contribution", "Type"])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 10px;
                gridline-color: {BORDER};
                color: {TEXT_DARK};
                font-size: 13px;
            }}
            QHeaderView::section {{
                background-color: #5A7D6A;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: 6px;
            }}
        """)

        layout.addWidget(self.table)

    def set_contributions(self, contributions: list[dict], contribution_type: str):
        self.table.setRowCount(len(contributions))

        for row, item in enumerate(contributions):
            feature = str(item.get("feature", "—"))
            contribution = float(item.get("contribution", 0))

            feature_item = QTableWidgetItem(feature)
            contribution_item = QTableWidgetItem(f"{contribution:.4f}")
            type_item = QTableWidgetItem(contribution_type)

            feature_item.setTextAlignment(Qt.AlignCenter)
            contribution_item.setTextAlignment(Qt.AlignCenter)
            type_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, feature_item)
            self.table.setItem(row, 1, contribution_item)
            self.table.setItem(row, 2, type_item)

    def clear(self):
        self.table.setRowCount(0)