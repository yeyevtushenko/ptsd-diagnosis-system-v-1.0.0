from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.styles.theme import button_style, drop_area_style


class FileUploader(QWidget):
    file_selected = Signal(str)

    def __init__(self):
        super().__init__()

        self.selected_file_path: str | None = None
        self.setAcceptDrops(True)

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        self.setLayout(layout)

        self.drop_label = QLabel("Drag and drop a CSV file here\n"
                                 "or\n"
                                 "Select a file using the button below")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet(drop_area_style())

        self.select_button = QPushButton("Select File")
        self.select_button.setStyleSheet(button_style())
        self.select_button.clicked.connect(self.select_file)

        layout.addWidget(self.drop_label)
        layout.addWidget(self.select_button)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )

        if file_path:
            self.set_file(file_path)

    def set_file(self, file_path: str):
        if not file_path.lower().endswith(".csv"):
            QMessageBox.warning(
                self,
                "Invalid File Format",
                "Please select a CSV file."
            )
            return

        self.selected_file_path = file_path
        self.drop_label.setText(f"Selected file:\n{Path(file_path).name}")
        self.file_selected.emit(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()

            if file_path.lower().endswith(".csv"):
                event.acceptProposedAction()
                return

        event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.set_file(file_path)
        event.acceptProposedAction()