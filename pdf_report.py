
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


PURPLE = colors.HexColor("#6D28D9")
DARK = colors.HexColor("#172033")
MUTED = colors.HexColor("#596579")
GREEN = colors.HexColor("#15803D")
RED = colors.HexColor("#BE123C")


def safe_text(value):
    """Escape text before placing it inside a ReportLab Paragraph."""
    return escape(str(value if value is not None else ""))


def build_pdf_report(result):
    """Build a downloadable PDF from the current analysis result."""
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.8 * cm,
        leftMargin=1.8 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.7 * cm,
        title="SkillNova Career Analysis Report",
        author="SkillNova",
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="BrandTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=31,
        textColor=PURPLE,
        alignment=TA_CENTER,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="SubtitleCustom",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceAfter=16,
    ))

    styles.add(ParagraphStyle(
        name="SectionCustom",
        parent=styles["Heading2"],
        fontSize=14,
        leading=18,
        textColor=PURPLE,
        spaceBefore=14,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
        textColor=DARK,
        spaceAfter=5,
        wordWrap="CJK",
    ))

    styles.add(ParagraphStyle(
        name="SmallCustom",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11,
        textColor=MUTED,
    ))

    story = []

    def add_section(title):
        story.append(Paragraph(safe_text(title), styles["SectionCustom"]))

    def add_body(text):
        story.append(Paragraph(safe_text(text), styles["BodyCustom"]))

    # Report heading
    story.append(Paragraph("SkillNova", styles["BrandTitle"]))
    story.append(Paragraph(
        "AI-Powered Skill Gap Analysis Report",
        styles["SubtitleCustom"],
    ))
    story.append(HRFlowable(
        width="100%",
        thickness=1.2,
        color=PURPLE,
        spaceAfter=14,
    ))

    analysis_id = result.get("analysis_id", "Not available")
    coverage = float(result.get("coverage", 0) or 0)

    add_body(f"Analysis reference ID: {analysis_id}")
    add_body("Purpose: Compare detected resume skills with the target job description.")

    # Summary table
    add_section("1. Analysis Summary")

    summary_data = [
        ["Metric", "Result"],
        ["Skill coverage", f"{coverage:.2f}%"],
        ["Required skills", str(len(result.get("required_skills", [])))],
        ["Matched skills", str(len(result.get("matched_skills", [])))],
        ["Skills to develop", str(len(result.get("missing_skills", [])))],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[8.2 * cm, 7.2 * cm],
        repeatRows=1,
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PURPLE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D9DCE5")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F7F7FC")),
        ("TEXTCOLOR", (0, 1), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Skills lists
    def add_skill_list(title, skills, color):
        add_section(title)

        if not skills:
            add_body("No skills listed.")
            return

        for skill in skills:
            story.append(Paragraph(
                f'<font color="{color.hexval()}">&#8226;</font> '
                f'{safe_text(skill)}',
                styles["BodyCustom"],
            ))

    add_skill_list(
        "2. Matched Skills",
        result.get("matched_skills", []),
        GREEN,
    )

    add_skill_list(
        "3. Skills to Develop",
        result.get("missing_skills", []),
        RED,
    )

    add_section("4. Required Skills")
    required_skills = result.get("required_skills", [])

    if required_skills:
        add_body(", ".join(str(skill) for skill in required_skills))
    else:
        add_body("No required skills were detected.")

    # Learning recommendations
    add_section("5. Personalized Learning Recommendations")
    recommendations = result.get("recommendations", [])

    if recommendations:
        for item in recommendations:
            story.append(Paragraph(
                safe_text(item.get("skill", "Recommended skill")).title(),
                styles["Heading3"],
            ))

            if item.get("priority") is not None:
                add_body(f"Priority: {item['priority']}")

            if item.get("resource"):
                add_body(f"Resource: {item['resource']}")

            if item.get("url"):
                add_body(f"Resource URL: {item['url']}")

            supporting = item.get("supporting_skills", [])
            if supporting:
                add_body(
                    "Related topics: " +
                    ", ".join(str(skill) for skill in supporting)
                )
    else:
        add_body("No additional recommendations are available.")

    # AI-generated learning roadmap
    add_section("6. AI-Powered Learning Roadmap")
    ai_plan = result.get("ai_plan") or {}

    if ai_plan.get("summary"):
        add_body(ai_plan["summary"])

    learning_plan = ai_plan.get("learning_plan", [])

    if learning_plan:
        for week in learning_plan:
            story.append(Paragraph(
                f"Week {safe_text(week.get('week', ''))}: "
                f"{safe_text(week.get('focus', 'Learning focus'))}",
                styles["Heading3"],
            ))

            skills = week.get("skills", [])
            add_body(
                "Skills: " + ", ".join(str(skill) for skill in skills)
            )

            activities = week.get("activities", [])
            if activities:
                add_body("Practice activities:")
                for activity in activities:
                    story.append(Paragraph(
                        f"&bull; {safe_text(activity)}",
                        styles["BodyCustom"],
                    ))

            if week.get("project"):
                add_body(f"Mini-project: {week['project']}")

            if week.get("outcome"):
                add_body(f"Expected outcome: {week['outcome']}")

    else:
        add_body("No learning roadmap is available for this analysis.")

    story.append(Spacer(1, 12))
    story.append(HRFlowable(
        width="100%",
        thickness=0.6,
        color=colors.HexColor("#D9DCE5"),
        spaceAfter=8,
    ))
    story.append(Paragraph(
        "Disclaimer: Skill coverage is based on keyword detection. "
        "It estimates detected skill overlap and does not measure actual "
        "proficiency or guarantee employment.",
        styles["SmallCustom"],
    ))

    def add_page_number(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(
            A4[0] / 2,
            0.9 * cm,
            f"SkillNova | Page {document.page}",
        )
        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    buffer.seek(0)
    return buffer
