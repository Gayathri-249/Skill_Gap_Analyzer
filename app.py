
import os
from io import BytesIO

from dotenv import load_dotenv

load_dotenv()

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    session,
    send_file,
)
from pypdf import PdfReader
from docx import Document

from skill_engine import (
    analyze_skill_gap,
    prioritized_recommendations,
)
from llm_engine import generate_learning_plan
from db import save_analysis, get_recent_analyses
from pdf_report import build_pdf_report


app = Flask(__name__)

# Flask session configuration
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "FLASK_SECRET_KEY is missing. "
        "Set it in your .env file or deployment environment."
    )

# Limit uploaded requests to 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


def extract_resume_text(file):
    """Extract text from PDF, DOCX, or TXT resumes."""
    filename = file.filename or ""

    if "." not in filename:
        raise ValueError(
            "Please upload a PDF, DOCX, or TXT resume."
        )

    extension = filename.rsplit(".", 1)[-1].lower()

    if extension not in {"pdf", "docx", "txt"}:
        raise ValueError(
            "Unsupported file type. Upload PDF, DOCX, or TXT."
        )

    file_bytes = BytesIO(file.read())

    if extension == "txt":
        return file_bytes.getvalue().decode(
            "utf-8",
            errors="replace"
        )

    if extension == "pdf":
        reader = PdfReader(file_bytes)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if extension == "docx":
        document = Document(file_bytes)
        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")

    resume_file = request.files.get("resume")
    job_description = request.form.get(
        "job_description", ""
    ).strip()

    job_title = request.form.get(
        "job_title", ""
    ).strip() or "AI Engineer"

    if not resume_file or not resume_file.filename:
        return render_template(
            "index.html",
            error="Please select your resume."
        ), 400

    if not job_description:
        return render_template(
            "index.html",
            error="Please enter the target job description."
        ), 400

    try:
        # 1. Extract text from the uploaded resume
        resume_filename = resume_file.filename
        resume_text = extract_resume_text(resume_file)

        if not resume_text.strip():
            return render_template(
                "index.html",
                error=(
                    "No readable text was found in the resume. "
                    "Scanned PDFs may require OCR."
                )
            ), 400

        # 2. Perform skill gap analysis
        result = analyze_skill_gap(
            resume_text,
            job_description
        )

        # 3. Validate detected job skills
        if not result["required_skills"]:
            return render_template(
                "index.html",
                error=(
                    "No supported skills were detected in the "
                    "job description. Try including explicit "
                    "skills such as Python, SQL, or NLP."
                )
            ), 400

        # 4. Generate prioritized learning recommendations
        result["recommendations"] = prioritized_recommendations(
            result["missing_skills"]
        )

        # 5. Generate the personalized AI learning roadmap
        result["ai_plan"] = generate_learning_plan(
            missing_skills=result["missing_skills"],
            target_role=job_title,
            current_skills=result["user_skills"],
            weeks=4,
        )

        # 6. Save the analysis to MySQL
        try:
            analysis_id = save_analysis(
                resume_filename=resume_filename,
                target_role=job_title,
                required_skills=result["required_skills"],
                matched_skills=result["matched_skills"],
                missing_skills=result["missing_skills"],
                coverage_percentage=result["coverage"],
            )

            result["analysis_id"] = analysis_id

            app.logger.info(
                "Analysis saved to MySQL with ID %s",
                analysis_id
            )

        except Exception:
            app.logger.exception(
                "Could not save analysis to MySQL."
            )

        # 7. NEW: Store the complete report in this browser session
        session["latest_result"] = result

        # 8. Display the complete skill gap report
        return render_template(
            "result.html",
            result=result
        )

    except ValueError as exc:
        return render_template(
            "index.html",
            error=str(exc)
        ), 400

    except Exception:
        app.logger.exception("Resume analysis failed")

        return render_template(
            "index.html",
            error=(
                "Unable to analyze this file. "
                "Check its format and try again."
            )
        ), 500


# NEW ROUTE: Download the latest analysis as a PDF
@app.route("/download-report", methods=["GET"])
def download_report():
    result = session.get("latest_result")

    if not result:
        return (
            "No analysis is available. Please analyze a resume first.",
            400,
        )

    try:
        pdf_buffer = build_pdf_report(result)

        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="SkillNova_Career_Analysis.pdf",
        )

    except Exception:
        app.logger.exception("Could not generate PDF report.")
        return (
            "Unable to generate the PDF report. Please try again.",
            500,
        )


@app.route("/history", methods=["GET"])
def history():
    """Display the most recent analyses stored in MySQL."""
    try:
        analyses = get_recent_analyses()
        return render_template(
            "history.html",
            analyses=analyses
        )

    except Exception:
        app.logger.exception(
            "Could not retrieve analysis history."
        )
        return (
            "Unable to load analysis history. "
            "Check the application logs.",
            500
        )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "application": "AI-Powered Skill Gap Analyzer",
        "phase": "Phase 4 - Database Integration"
    })


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error="Request too large. Maximum allowed size is 5 MB."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
