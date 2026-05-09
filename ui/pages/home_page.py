from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ui.styles.theme import BORDER, PRIMARY_COLOR, SURFACE, TEXT_DARK, TEXT_MUTED


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {SURFACE};
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        self.setLayout(layout)

        title = QLabel("PTSD Diagnosis System Based on BOLD Signals")
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
            "This software application analyzes statistical parameters of BOLD signal "
            "cross-correlation functions and supports PTSD-related classification using "
            "a trained logistic regression model."
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

        cards_layout = QGridLayout()
        cards_layout.setSpacing(16)

        cards_layout.addWidget(
            self._create_info_card(
                "Input",
                "Patient CSV file containing cross-correlation functions of BOLD signals."
            ),
            0,
            0
        )

        cards_layout.addWidget(
            self._create_info_card(
                "Processing",
                "Validation, extraction of x1–x20 statistical features, feature transformation, and classification."
            ),
            0,
            1
        )

        cards_layout.addWidget(
            self._create_info_card(
                "Output",
                "Prediction probability, model explanation, feature heatmap, and exportable reports."
            ),
            0,
            2
        )

        workflow_title = QLabel("System Workflow")
        workflow_title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 20px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }}
        """)

        workflow = QLabel(
            "System workflow:\n"
            "1. Upload a patient CSV file.\n"
            "2. Validate the input data structure.\n"
            "3. Extract base statistical features x1–x20.\n"
            "4. Generate transformed predictors.\n"
            "5. Run logistic regression prediction.\n"
            "6. Explain the model decision and visualize feature contributions."
        )
        workflow.setWordWrap(True)
        workflow.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 15px;
                padding: 14px;
                background-color: #F6F8F4;
                border: 1px solid {BORDER};
                border-radius: 12px;
            }}
        """)

        note = QLabel(
            "Note: This application is developed as a research software tool and is not intended "
            "to replace professional clinical diagnosis."
        )
        note.setWordWrap(True)
        note.setStyleSheet("""
            QLabel {
                color: #6F7D73;
                font-size: 13px;
                padding: 10px;
                background-color: transparent;
                border: none;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(cards_layout)
        layout.addWidget(workflow_title)
        layout.addWidget(workflow)
        layout.addWidget(note)
        layout.addStretch()

    def _create_info_card(self, title: str, text: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #F6F8F4;
                border: 1px solid {BORDER};
                border-radius: 14px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)
        card.setLayout(layout)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {PRIMARY_COLOR};
                font-size: 17px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }}
        """)

        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 14px;
                background-color: transparent;
                border: none;
            }}
        """)

        layout.addWidget(title_label)
        layout.addWidget(text_label)

        return card