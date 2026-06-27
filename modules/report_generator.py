from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.units import inch


def generate_pdf_report(
    df,
    problem_type,
    target,
    plan,
    scores,
    best,
    reflection,
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    # -------------------------------------------------
    # Title
    # -------------------------------------------------
    elements.append(
        Paragraph("<b><font size=18>StatAgent AI Report</font></b>", styles["Title"])
    )

    elements.append(Spacer(1, 0.3 * inch))

    # -------------------------------------------------
    # Dataset Summary
    # -------------------------------------------------
    elements.append(Paragraph("<b>Dataset Summary</b>", styles["Heading2"]))

    elements.append(
        Paragraph(f"Rows : {df.shape[0]}", styles["BodyText"])
    )

    elements.append(
        Paragraph(f"Columns : {df.shape[1]}", styles["BodyText"])
    )

    elements.append(
        Paragraph(
            f"Features : {', '.join(df.columns)}",
            styles["BodyText"],
        )
    )

    elements.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # Problem Information
    # -------------------------------------------------
    elements.append(
        Paragraph("<b>Problem Identification</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(f"Target Variable : {target}", styles["BodyText"])
    )

    elements.append(
        Paragraph(f"Detected Problem : {problem_type}", styles["BodyText"])
    )

    elements.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # Planning Agent
    # -------------------------------------------------
    elements.append(
        Paragraph("<b>Planning Agent</b>", styles["Heading2"])
    )

    for step in plan:
        elements.append(
            Paragraph(f"• {step}", styles["BodyText"])
        )

    elements.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # Model Scores
    # -------------------------------------------------
    elements.append(
        Paragraph("<b>Model Evaluation</b>", styles["Heading2"])
    )

    for model, score in scores.items():

        elements.append(
            Paragraph(
                f"{model} : {score:.4f}",
                styles["BodyText"]
            )
        )

    elements.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # Best Model
    # -------------------------------------------------
    elements.append(
        Paragraph("<b>Best Model</b>", styles["Heading2"])
    )

    elements.append(
        Paragraph(
            f"{best['best_model']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Score : {best['best_score']:.4f}",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # Reflection
    # -------------------------------------------------
    elements.append(
        Paragraph("<b>Reflection Agent</b>", styles["Heading2"])
    )

    # Replace newlines so ReportLab formats correctly
    reflection = reflection.replace("\n", "<br/>")

    elements.append(
        Paragraph(reflection, styles["BodyText"])
    )

    elements.append(Spacer(1, 0.2 * inch))

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------
    elements.append(
        Paragraph(
            "Generated automatically by StatAgent AI",
            styles["Italic"],
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf