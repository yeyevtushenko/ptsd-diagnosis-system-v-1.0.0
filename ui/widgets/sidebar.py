from __future__ import annotations

import qtawesome as qta

from PySide6.QtCore import Signal, QSize
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from ui.styles.theme import PRIMARY_COLOR, PRIMARY_HOVER, TEXT_DARK, SURFACE


class Sidebar(QWidget):
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedWidth(260)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {SURFACE};
                border-right: 1px solid #D6DED2;
            }}
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 20, 16, 20)
        self.setLayout(layout)

        title_container = QWidget()

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(12)

        title_container.setLayout(title_layout)

        brain_icon = QLabel()
        brain_icon.setPixmap(
            qta.icon(
                "fa5s.brain",
                color=TEXT_DARK
            ).pixmap(36, 36)
        )

        title = QLabel("PTSD\nDiagnosis System")
        title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 20px;
                font-weight: bold;
                border: none;
            }}
        """)

        title_layout.addWidget(brain_icon)
        title_layout.addWidget(title)

        layout.addWidget(title_container)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #D6DED2;")
        layout.addWidget(separator)

        self.home_button = self._create_button(
            "Overview",
            "home",
            qta.icon("fa5s.home", color=TEXT_DARK)
        )

        self.upload_button = self._create_button(
            "Upload Data",
            "upload",
            qta.icon("fa5s.upload", color=TEXT_DARK)
        )

        self.results_button = self._create_button(
            "Results",
            "results",
            qta.icon("fa5s.chart-bar", color=TEXT_DARK)
        )

        self.explanation_button = self._create_button(
            "Feature Analysis",
            "explanation",
            qta.icon("fa5s.brain", color=TEXT_DARK)
        )

        self.heatmap_button = self._create_button(
            "Heatmap",
            "heatmap",
            qta.icon("fa5s.th", color=TEXT_DARK)
        )

        self.model_button = self._create_button(
            "FAQ && Model",
            "model_info",
            qta.icon("fa5s.info-circle", color=TEXT_DARK)

        )

        layout.addWidget(self.home_button)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.results_button)
        layout.addWidget(self.explanation_button)
        layout.addWidget(self.heatmap_button)
        layout.addWidget(self.model_button)

        layout.addStretch()

        version_label = QLabel("v1.0.0 BETA")
        version_label.setStyleSheet(f"""
            QLabel {{
                color: #7A8A80;
                font-size: 12px;
                border: none;
                padding: 6px;
            }}
        """)

        layout.addWidget(version_label)

    def _create_button(self, text: str, page_name: str, icon) -> QPushButton:
        button = QPushButton(icon, text)
        button.setIconSize(QSize(18, 18))
        button.setStyleSheet(self._button_style())
        button.clicked.connect(lambda: self.page_changed.emit(page_name))
        return button

    def _button_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {TEXT_DARK};
                border: none;
                border-radius: 8px;
                padding: 12px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY_HOVER};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: {PRIMARY_COLOR};
                color: white;
            }}
        """