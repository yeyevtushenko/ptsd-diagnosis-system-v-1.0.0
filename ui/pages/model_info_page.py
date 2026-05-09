from __future__ import annotations

import json

from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config.paths import MODEL_METADATA_PATH
from ui.styles.theme import (
    BORDER,
    PRIMARY_COLOR,
    SURFACE,
    TEXT_DARK,
    TEXT_MUTED,
    text_box_style,
)


class ModelInfoPage(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.load_model_info()

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)
        self.setLayout(layout)

        title = QLabel("FAQ & Model Information")
        title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 26px;
                font-weight: bold;
            }}
        """)

        description = QLabel(
            "This section provides technical information about the classification model "
            "and explains how to interpret the analysis results."
        )
        description.setWordWrap(True)
        description.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 15px;
            }}
        """)

        self.model_summary_grid = QGridLayout()
        self.model_summary_grid.setSpacing(14)

        self.model_name_card = self._create_metric_card("Model Name", "—")
        self.model_type_card = self._create_metric_card("Model Type", "—")
        self.target_card = self._create_metric_card("Target", "—")
        self.status_card = self._create_metric_card("Status", "—")

        self.model_summary_grid.addWidget(self.model_name_card, 0, 0)
        self.model_summary_grid.addWidget(self.model_type_card, 0, 1)
        self.model_summary_grid.addWidget(self.target_card, 1, 0)
        self.model_summary_grid.addWidget(self.status_card, 1, 1)

        details_label = QLabel("Technical Details")
        details_label.setStyleSheet(self._section_label_style())

        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setStyleSheet(text_box_style())
        self.text_box.setMaximumHeight(190)

        faq_label = QLabel("FAQ")
        faq_label.setStyleSheet(self._section_label_style())

        faq_box = self._create_faq_box()

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(self.model_summary_grid)
        layout.addWidget(details_label)
        layout.addWidget(self.text_box)
        layout.addWidget(faq_label)
        layout.addWidget(faq_box)
        layout.addStretch()

    def _section_label_style(self) -> str:
        return f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 18px;
                font-weight: bold;
            }}
        """

    def _create_metric_card(self, label: str, value: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 14px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)
        card.setLayout(layout)

        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 13px;
                border: none;
            }}
        """)

        value_widget = QLabel(value)
        value_widget.setWordWrap(True)
        value_widget.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 18px;
                font-weight: bold;
                border: none;
            }}
        """)

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)

        card.value_widget = value_widget
        return card

    def _create_faq_box(self) -> QFrame:
        box = QFrame()
        box.setStyleSheet(f"""
            QFrame {{
                background-color: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 16px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(12)
        box.setLayout(layout)

        faq_items = [
            (
                "What does Class 1 mean?",
                "Class 1 corresponds to the PTSD group, while Class 0 corresponds to the control group."
            ),
            (
                "What does Confidence mean?",
                "Confidence is the probability of the class predicted by the model."
            ),
            (
                "What is Model Score?",
                "Model Score is the linear output of the logistic regression before applying the sigmoid function."
            ),
            (
                "What does the heatmap show?",
                "The heatmap visualizes how transformed predictors contribute to the final model decision."
            ),
            (
                "Can this system replace clinical diagnosis?",
                "No. This application is a research software tool and should not replace professional clinical assessment."
            ),
        ]

        for question, answer in faq_items:
            question_label = QLabel(question)
            question_label.setStyleSheet(f"""
                QLabel {{
                    color: {PRIMARY_COLOR};
                    font-size: 15px;
                    font-weight: bold;
                    border: none;
                }}
            """)

            answer_label = QLabel(answer)
            answer_label.setWordWrap(True)
            answer_label.setStyleSheet(f"""
                QLabel {{
                    color: {TEXT_MUTED};
                    font-size: 14px;
                    border: none;
                }}
            """)

            layout.addWidget(question_label)
            layout.addWidget(answer_label)

        return box

    def load_model_info(self):
        try:
            with open(MODEL_METADATA_PATH, "r", encoding="utf-8") as file:
                metadata = json.load(file)
        except Exception as e:
            self.text_box.setText(f"Failed to load model information:\n{e}")
            return

        self.model_name_card.value_widget.setText(str(metadata.get("model_name", "—")))
        self.model_type_card.value_widget.setText(str(metadata.get("model_type", "—")))
        self.target_card.value_widget.setText(str(metadata.get("target", "—")))
        self.status_card.value_widget.setText(str(metadata.get("status", "—")))

        lines = []

        lines.append(f"Description: {metadata.get('description', '—')}")
        lines.append("")
        lines.append(f"Number of base features used by the model: {metadata.get('base_feature_count', '—')}")
        lines.append(f"Full base feature space: {metadata.get('source_feature_pool', '—')}")

        training_params = metadata.get("training_parameters", {})
        lines.append("")
        lines.append("Training parameters:")
        lines.append(f"test_size: {training_params.get('test_size', '—')}")
        lines.append(f"valid_size: {training_params.get('valid_size', '—')}")

        artifacts = metadata.get("artifacts", {})
        lines.append("")
        lines.append("Related files:")
        for key, value in artifacts.items():
            lines.append(f"{key}: {value}")

        self.text_box.setText("\n".join(lines))