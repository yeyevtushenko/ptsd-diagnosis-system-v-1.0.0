from __future__ import annotations

from PySide6.QtCore import QObject, Signal, Slot

from backend.controllers.app_controller import AppController


class AnalysisWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, file_path: str):
        super().__init__()

        self.file_path = file_path
        self.controller = AppController()

    @Slot()
    def run(self):
        try:
            result = self.controller.analyze_patient(self.file_path)
            self.finished.emit(result)

        except Exception as e:
            self.error.emit(str(e))
