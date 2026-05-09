from __future__ import annotations

from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget

from ui.styles.theme import PRIMARY_COLOR, TEXT_MUTED


class ProgressStatus(QWidget):
    def __init__(self):
        super().__init__()

        self.animation: QPropertyAnimation | None = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        self.setLayout(layout)

        self.status_label = QLabel("Waiting for CSV file")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 14px;
            }}
        """)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #C8D2C5;
                border-radius: 8px;
                text-align: center;
                height: 20px;
                background-color: #F6F8F4;
            }}
            QProgressBar::chunk {{
                background-color: {PRIMARY_COLOR};
                border-radius: 8px;
            }}
        """)

        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

    def animate_to(
        self,
        value: int,
        text: str = "",
        duration: int = 700,
        finished_callback=None
    ):
        if text:
            self.status_label.setText(text)

        if self.animation:
            self.animation.stop()

        self.animation = QPropertyAnimation(self.progress_bar, b"value")
        self.animation.setDuration(duration)
        self.animation.setStartValue(self.progress_bar.value())
        self.animation.setEndValue(value)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

        if finished_callback:
            self.animation.finished.connect(finished_callback)

        self.animation.start()

    def reset(self):
        self.progress_bar.setValue(0)
        self.status_label.setText("Waiting for CSV file")

    def file_selected(self):
        self.animate_to(20, "CSV file selected", 500)

    def analysis_started(self):
        self.animate_to(45, "Validating File", 500)

    def analysis_processing(self):
        self.animate_to(80, "Extracting Features and Running Classification", 900)

    def analysis_finished(self, finished_callback=None):
        self.animate_to(
            100,
            "Analysis Completed",
            700,
            finished_callback=finished_callback
        )

    def analysis_failed(self):
        self.animate_to(0, "Analysis Failed", 500)