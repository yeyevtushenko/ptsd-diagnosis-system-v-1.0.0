from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def save_result_to_json(result: Dict[str, Any], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    return output_path


def save_result_to_pdf(result: Dict[str, Any], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    prediction = result.get("prediction", {})
    explanation = result.get("explanation", {})

    predicted_class = int(prediction.get("predicted_class", 0))
    probability_class_1 = float(prediction.get("probability_class_1", prediction.get("probability", 0)))
    probability_class_0 = float(prediction.get("probability_class_0", 1 - probability_class_1))
    confidence = float(
        prediction.get("predicted_probability", probability_class_1 if predicted_class == 1 else probability_class_0))

    class_label = "PTSD / Class 1" if predicted_class == 1 else "Control / Class 0"

    story.append(Paragraph("PTSD Analysis Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Paragraph(f"Patient file: {result.get('patient', '-')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Prediction Summary", styles["Heading2"]))

    prediction_data = [
        ["Parameter", "Value"],
        ["Predicted class", class_label],
        ["Confidence", f"{confidence * 100:.2f}%"],
        ["Probability of Class 1", f"{probability_class_1 * 100:.2f}%"],
        ["Probability of Class 0", f"{probability_class_0 * 100:.2f}%"],
        ["Model score", f"{float(prediction.get('z', 0)):.4f}"],
        ["Decision threshold", f"{float(prediction.get('threshold', 0)):.2f}"],
    ]

    story.append(_build_table(prediction_data))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Model Explanation", styles["Heading2"]))
    story.append(Paragraph(explanation.get("summary", "-"), styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Top Positive Contributions", styles["Heading2"]))
    story.append(_build_contribution_table(explanation.get("top_positive_contributions", [])))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Top Negative Contributions", styles["Heading2"]))
    story.append(_build_contribution_table(explanation.get("top_negative_contributions", [])))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Base Features x1-x20", styles["Heading2"]))
    story.append(_build_feature_table(result.get("base_features", {})))

    doc.build(story)
    return output_path


def _build_table(data: list[list[str]]) -> Table:
    table = Table(data, hAlign="LEFT")

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5A7D6A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8D2C5")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    return table


def _build_contribution_table(contributions: list[dict]) -> Table:
    data = [["Feature", "Contribution"]]

    for item in contributions[:10]:
        data.append([
            str(item.get("feature", "-")),
            f"{float(item.get('contribution', 0)):.4f}",
        ])

    return _build_table(data)


def _build_feature_table(features: Dict[str, float]) -> Table:
    data = [["Feature", "Value"]]

    for name, value in features.items():
        data.append([name, f"{float(value):.6f}"])

    return _build_table(data)