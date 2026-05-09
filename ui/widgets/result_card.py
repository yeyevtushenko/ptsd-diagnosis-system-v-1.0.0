from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ui.styles.theme import (
    BORDER,
    SURFACE,
    TEXT_DARK,
    TEXT_MUTED,
)


class ResultCard(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {SURFACE};
                border: 1px solid {BORDER};
                border-radius: 16px;
            }}
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(22, 22, 22, 22)
        self.layout.setSpacing(16)
        self.setLayout(self.layout)

        self.title = QLabel("Analysis Result")
        self.title.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 22px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }}
        """)

        self.status_label = QLabel("No result yet")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(self._status_style("#EEF3EE", TEXT_DARK))

        self.metrics_grid = QGridLayout()
        self.metrics_grid.setSpacing(14)

        self.class_card = self._create_metric_card("Predicted Class", "—")
        self.probability_card = self._create_metric_card("Confidence", "—")
        self.z_card = self._create_metric_card("Model Score", "—")
        self.threshold_card = self._create_metric_card("Decision Threshold", "—")

        self.metrics_grid.addWidget(self.class_card, 0, 0)
        self.metrics_grid.addWidget(self.probability_card, 0, 1)
        self.metrics_grid.addWidget(self.z_card, 1, 0)
        self.metrics_grid.addWidget(self.threshold_card, 1, 1)

        self.summary = QLabel("Run an analysis to generate results.")
        self.summary.setWordWrap(True)
        self.summary.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 14px;
                background-color: transparent;
                border: none;
                padding: 8px;
            }}
        """)

        self.top_features = QLabel("")
        self.top_features.setWordWrap(True)
        self.top_features.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 14px;
                background-color: transparent;
                border: none;
                padding: 8px;
            }}
        """)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.status_label)
        self.layout.addLayout(self.metrics_grid)
        self.layout.addWidget(self.summary)
        self.layout.addWidget(self.top_features)
        self.layout.addStretch()

    def _status_style(self, background: str, color: str) -> str:
        return f"""
            QLabel {{
                background-color: {background};
                color: {color};
                border: none;
                border-radius: 12px;
                padding: 14px;
                font-size: 18px;
                font-weight: bold;
            }}
        """

    def _create_metric_card(self, label: str, value: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #F6F8F4;
                border: 1px solid {BORDER};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)
        card.setLayout(layout)

        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_MUTED};
                font-size: 13px;
                background-color: transparent;
                border: none;
            }}
        """)

        value_widget = QLabel(value)
        value_widget.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DARK};
                font-size: 20px;
                font-weight: bold;
                background-color: transparent;
                border: none;
            }}
        """)

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)

        card.value_widget = value_widget
        return card

    def clear(self):
        self.status_label.setText("No result yet")
        self.status_label.setStyleSheet(self._status_style("#EEF3EE", TEXT_DARK))

        self.class_card.value_widget.setText("—")
        self.probability_card.value_widget.setText("—")
        self.z_card.value_widget.setText("—")
        self.threshold_card.value_widget.setText("—")

        self.summary.setText("Run an analysis to generate results.")
        self.top_features.setText("")

    def show_loading(self):
        self.clear()
        self.status_label.setText("Analysis in progress...")

    def show_error(self, stage: str, message: str):
        self.clear()
        self.status_label.setText("Analysis Failed")
        self.status_label.setStyleSheet(self._status_style("#F8D7DA", "#842029"))
        self.summary.setText(f"Stage: {stage}\n\n{message}")

    def show_result(self, result: dict):
        prediction = result["prediction"]
        explanation = result["explanation"]

        predicted_class = int(prediction["predicted_class"])

        probability_class_1 = float(prediction["probability_class_1"])
        probability_class_0 = float(prediction["probability_class_0"])
        confidence = float(prediction["predicted_probability"])

        z_score = float(prediction["z"])
        threshold = float(prediction["threshold"])

        if predicted_class == 1:
            class_text = "PTSD / Class 1"
            status_text = "Class 1 Detected"
            status_background = "#DFF3E4"
            status_color = "#1F5132"
        else:
            class_text = "Control / Class 0"
            status_text = "Class 0 Detected"
            status_background = "#E8F0F2"
            status_color = "#244B5A"

        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(
            self._status_style(status_background, status_color)
        )

        self.class_card.value_widget.setText(class_text)
        self.probability_card.value_widget.setText(f"{confidence * 100:.2f}%")
        self.z_card.value_widget.setText(f"{z_score:.4f}")
        self.threshold_card.value_widget.setText(f"{threshold:.2f}")

        self.summary.setText(
            f"File: {result['patient']}\n\n"
            f"Probability of Class 1: {probability_class_1 * 100:.2f}%\n"
            f"Probability of Class 0: {probability_class_0 * 100:.2f}%\n\n"
            f"The confidence value shows the probability of the predicted class."
        )

        positive = explanation["top_positive_contributions"][:3]
        negative = explanation["top_negative_contributions"][:3]

        lines = []
        lines.append("Top Positive Contributions:")
        for item in positive:
            lines.append(f"  + {item['feature']}: {item['contribution']:.4f}")

        lines.append("")
        lines.append("Top Negative Contributions:")
        for item in negative:
            lines.append(f"  - {item['feature']}: {item['contribution']:.4f}")

        self.top_features.setText("\n".join(lines))