from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


class PTSDApplication:
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def run(self):
        self.main_window.show()
        return self.qt_app.exec()


def create_app() -> PTSDApplication:
    return PTSDApplication()