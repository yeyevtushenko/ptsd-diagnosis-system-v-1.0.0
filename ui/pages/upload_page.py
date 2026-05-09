from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
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
from ui.widgets.file_uploader import FileUploader
from ui.widgets.progress_status import ProgressStatus


class UploadPage(QWidget):
    analysis_requested = Signal(str)

    def __init__(self):
        super().__init__()

        self.selected_file_path: str | None = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)
        self.setLayout(layout)

        title = QLabel("Data Upload")
        title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 26px;
                font-weight: bold;
            }}
        """)

        description = QLabel(
            "Upload a patient CSV file containing cross-correlation functions "
            "of BOLD signals. The system will validate the file, extract features, "
            "run classification, and generate interpretable results."
        )
        description.setWordWrap(True)
        description.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 15px;
            }}
        """)

        info_card = self._create_info_card()

        self.file_uploader = FileUploader()
        self.file_uploader.file_selected.connect(self.on_file_selected)

        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 14px;
            }}
        """)

        self.progress_status = ProgressStatus()

        self.analyze_button = QPushButton("Run Analysis")
        self.analyze_button.setStyleSheet(button_style())
        self.analyze_button.clicked.connect(self.request_analysis)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(info_card)
        layout.addWidget(self.file_uploader)
        layout.addWidget(self.file_label)
        layout.addWidget(self.progress_status)
        layout.addWidget(self.analyze_button)
        layout.addStretch()

    def _create_info_card(self) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 16px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(10)
        card.setLayout(layout)

        title = QLabel("Expected CSV Format")
        title.setStyleSheet(f"""
            QLabel {{
                color: {PRIMARY_COLOR};
                font-size: 17px;
                font-weight: bold;
                border: none;
            }}
        """)

        text = QLabel(
            "• One CSV file should correspond to one patient.\n"
            "• Columns should represent ROI pairs used by the trained model.\n"
            "• Rows should contain cross-correlation function values.\n"
            "• The file must match the ROI configuration defined in feature_config.json."
        )
        text.setWordWrap(True)
        text.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 14px;
                border: none;
            }}
        """)

        layout.addWidget(title)
        layout.addWidget(text)

        return card

    def on_file_selected(self, file_path: str):
        self.selected_file_path = file_path
        self.file_label.setText(f"Selected file: {file_path}")
        self.progress_status.file_selected()

    def request_analysis(self):
        if not self.selected_file_path:
            QMessageBox.warning(
                self,
                "No File Selected",
                "Please select or drag and drop a CSV file first."
            )
            return

        self.progress_status.analysis_started()
        self.analysis_requested.emit(self.selected_file_path)

    def mark_analysis_processing(self):
        self.progress_status.analysis_processing()

    def mark_analysis_finished(self, finished_callback=None):
        self.progress_status.analysis_finished(
            finished_callback=finished_callback
        )

    def mark_analysis_failed(self):
        self.progress_status.analysis_failed()

    def reset_progress(self):
        self.progress_status.reset()