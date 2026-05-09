from __future__ import annotations

import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.styles.theme import BACKGROUND, TEXT_DARK


class PTSDApplication:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.app.setStyle("Fusion")

        font = QFont("Arial")
        font.setPointSize(10)
        self.app.setFont(font)

        self.app.setStyleSheet(f"""
            QWidget {{
                font-family: Arial;
                color: {TEXT_DARK};
                background-color: {BACKGROUND};
            }}

            QLabel {{
                background-color: transparent;
            }}

            QFrame {{
                background-color: transparent;
            }}
        """)

        self.main_window = MainWindow()

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec())


def create_app():
    return PTSDApplication()