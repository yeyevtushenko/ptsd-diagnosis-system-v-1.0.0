from __future__ import annotations

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QWidget,
    QStackedWidget,
)

from backend.controllers.app_controller import AppController

from ui.widgets.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.upload_page import UploadPage
from ui.pages.result_page import ResultPage
from ui.pages.explanation_page import ExplanationPage
from ui.pages.heatmap_page import HeatmapPage
from ui.pages.model_info_page import ModelInfoPage
from ui.workers.analysis_worker import AnalysisWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = AppController()
        self.last_result: dict | None = None
        self.analysis_thread: QThread | None = None
        self.analysis_worker: AnalysisWorker | None = None

        self.setWindowTitle("PTSD Diagnosis System")
        self.resize(1200, 780)

        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(root_layout)

        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.show_page)

        self.pages = QStackedWidget()

        self.home_page = HomePage()
        self.upload_page = UploadPage()
        self.result_page = ResultPage()
        self.explanation_page = ExplanationPage()
        self.heatmap_page = HeatmapPage()
        self.model_info_page = ModelInfoPage()

        self.upload_page.analysis_requested.connect(self.run_analysis)

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.upload_page)
        self.pages.addWidget(self.result_page)
        self.pages.addWidget(self.explanation_page)
        self.pages.addWidget(self.heatmap_page)
        self.pages.addWidget(self.model_info_page)

        self.page_indexes = {
            "home": 0,
            "upload": 1,
            "results": 2,
            "explanation": 3,
            "heatmap": 4,
            "model_info": 5,
        }

        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.pages)

        self.show_page("home")

    def show_page(self, page_name: str):
        index = self.page_indexes.get(page_name, 0)
        self.pages.setCurrentIndex(index)

    def run_analysis(self, file_path: str):
        self.upload_page.mark_analysis_processing()

        self.analysis_thread = QThread()
        self.analysis_worker = AnalysisWorker(file_path)

        self.analysis_worker.moveToThread(self.analysis_thread)

        self.analysis_thread.started.connect(self.analysis_worker.run)

        self.analysis_worker.finished.connect(self.on_analysis_finished)
        self.analysis_worker.error.connect(self.on_analysis_error)

        self.analysis_worker.finished.connect(self.analysis_thread.quit)
        self.analysis_worker.error.connect(self.analysis_thread.quit)

        self.analysis_worker.finished.connect(self.analysis_thread.deleteLater)
        self.analysis_worker.error.connect(self.analysis_thread.deleteLater)

        self.analysis_thread.start()

    def on_analysis_finished(self, result: dict):
        if result["status"] == "error":
            self.upload_page.mark_analysis_failed()

            message = ""

            if "errors" in result:
                message += "\n".join(result["errors"])

            if "message" in result:
                message += result["message"]

            self.result_page.show_error(result["stage"], message)

            self.upload_page.progress_status.animate_to(
                100,
                "Аналіз завершено з помилкою",
                600,
                finished_callback=lambda: self.show_page("results")
            )
            return

        self.last_result = result

        self.result_page.show_result(result)
        self.explanation_page.show_explanation(result)
        self.heatmap_page.show_heatmap(result)

        self.upload_page.mark_analysis_finished(
            finished_callback=lambda: self.show_page("results")
        )

    def on_analysis_error(self, message: str):
        self.upload_page.mark_analysis_failed()
        self.result_page.show_error("analysis error", message)

        self.upload_page.progress_status.animate_to(
            100,
            "Аналіз завершено з помилкою",
            600,
            finished_callback=lambda: self.show_page("results")
        )
