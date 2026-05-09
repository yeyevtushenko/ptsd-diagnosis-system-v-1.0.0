from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.styles.theme import (
    BORDER,
    PRIMARY_COLOR,
    SURFACE,
    TEXT_DARK,
    TEXT_MUTED,
    button_style,
)
from ui.widgets.result_card import ResultCard
from utils.report_utils import save_result_to_json, save_result_to_pdf


class ResultPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_result: dict | None = None
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {SURFACE};
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)
        self.setLayout(layout)

        title = QLabel("Classification Results")
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
            "This page displays the patient analysis result, the estimated PTSD class "
            "probability, and the main predictor contributions."
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

        self.export_json_button = QPushButton("Export JSON")
        self.export_json_button.setStyleSheet(button_style())
        self.export_json_button.clicked.connect(self.export_json)
        self.export_json_button.hide()

        self.export_pdf_button = QPushButton("Export PDF")
        self.export_pdf_button.setStyleSheet(button_style())
        self.export_pdf_button.clicked.connect(self.export_pdf)
        self.export_pdf_button.hide()

        header_actions = QHBoxLayout()
        header_actions.setSpacing(12)
        header_actions.addStretch()
        header_actions.addWidget(self.export_json_button)
        header_actions.addWidget(self.export_pdf_button)
        header_actions.addStretch()

        self.empty_state = self._create_empty_state()

        self.result_card = ResultCard()
        self.result_card.hide()

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(header_actions)
        layout.addWidget(self.empty_state)
        layout.addWidget(self.result_card)
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

        icon = QLabel("📊")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("""
            QLabel {
                font-size: 42px;
                background-color: transparent;
                border: none;
            }
        """)

        title = QLabel("No analysis results yet")
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
            "Upload a patient CSV file and run the analysis to generate:\n\n"
            "• PTSD class probability\n"
            "• model decision explanation\n"
            "• top predictor contributions\n"
            "• exportable JSON and PDF reports"
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

        hint = QLabel("Go to Upload Data to start a new analysis.")
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

    def _set_export_visible(self, visible: bool):
        self.export_json_button.setVisible(visible)
        self.export_pdf_button.setVisible(visible)

    def show_loading(self):
        self.current_result = None
        self.empty_state.hide()
        self.result_card.show()
        self.result_card.clear()
        self.result_card.show_loading()
        self._set_export_visible(False)

    def show_error(self, stage: str, message: str):
        self.current_result = None
        self.empty_state.hide()
        self.result_card.show()
        self.result_card.show_error(stage, message)
        self._set_export_visible(False)

    def show_result(self, result: dict):
        self.current_result = result
        self.empty_state.hide()
        self.result_card.show()
        self.result_card.show_result(result)
        self._set_export_visible(True)

    def export_json(self):
        if not self.current_result:
            QMessageBox.warning(
                self,
                "No Results Available",
                "Please run the patient analysis first."
            )
            return

        patient = self.current_result.get("patient", "patient")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"report_{patient}_{timestamp}.json"

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON Report",
            str(Path("data/output") / default_name),
            "JSON Files (*.json)"
        )

        if not output_path:
            return

        if not output_path.lower().endswith(".json"):
            output_path += ".json"

        try:
            saved_path = save_result_to_json(self.current_result, output_path)
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))
            return

        QMessageBox.information(
            self,
            "Export Completed",
            f"JSON report has been saved:\n{saved_path}"
        )

    def export_pdf(self):
        if not self.current_result:
            QMessageBox.warning(
                self,
                "No Results Available",
                "Please run the patient analysis first."
            )
            return

        patient = self.current_result.get("patient", "patient")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"report_{patient}_{timestamp}.pdf"

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            str(Path("data/output") / default_name),
            "PDF Files (*.pdf)"
        )

        if not output_path:
            return

        if not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"

        try:
            saved_path = save_result_to_pdf(self.current_result, output_path)
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))
            return

        QMessageBox.information(
            self,
            "Export Completed",
            f"PDF report has been saved:\n{saved_path}"
        )