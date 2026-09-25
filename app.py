"""
Smart Resume Analyzer with AI-Based Feedback
Main Flask Web Application
"""

import os
import io
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from parser import ResumeParser
from analyzer import ResumeAnalyzer
from models import init_db, save_analysis, get_recent_analyses, get_analysis_by_id
from roles_data import JOB_ROLES

import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.secret_key = "skillorbit-resume-analyzer-secure-key"

# Handle writable upload directory for Vercel/serverless environments
if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    app.config["UPLOAD_FOLDER"] = os.path.join(tempfile.gettempdir(), "uploads")
else:
    try:
        local_upload = os.path.join(BASE_DIR, "static", "uploads")
        os.makedirs(local_upload, exist_ok=True)
        app.config["UPLOAD_FOLDER"] = local_upload
    except (OSError, PermissionError):
        app.config["UPLOAD_FOLDER"] = os.path.join(tempfile.gettempdir(), "uploads")

try:
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
except Exception:
    pass

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}

try:
    init_db()
except Exception as e:
    print(f"Database init notice: {e}")

parser = ResumeParser()
analyzer = ResumeAnalyzer()

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    roles = list(JOB_ROLES.keys())
    return render_template("index.html", roles=roles)

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    target_role = request.form.get("target_role", "AI Engineer")
    sample_type = request.form.get("sample_type", None)

    # Check if user selected one of the instant sample resumes
    if sample_type:
        sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_resumes", f"sample_{sample_type}.txt")
        if os.path.exists(sample_path):
            parsed_data = parser.parse(sample_path)
            analysis_result = analyzer.analyze(parsed_data, target_role)
            record_id = save_analysis(analysis_result)
            return redirect(url_for("view_dashboard", analysis_id=record_id))

    if "resume_file" not in request.files:
        flash("No file part uploaded. Please select a resume file.", "warning")
        return redirect(url_for("index"))

    file = request.files["resume_file"]
    if file.filename == "":
        flash("No file selected. Please choose a PDF, DOCX, or TXT resume.", "warning")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        try:
            parsed_data = parser.parse(save_path)
            analysis_result = analyzer.analyze(parsed_data, target_role)
            record_id = save_analysis(analysis_result)
            return redirect(url_for("view_dashboard", analysis_id=record_id))
        except Exception as e:
            flash(f"Error parsing resume: {str(e)}", "danger")
            return redirect(url_for("index"))
    else:
        flash("Invalid file extension. Please upload .pdf, .docx, or .txt documents.", "danger")
        return redirect(url_for("index"))

@app.route("/dashboard/<int:analysis_id>")
def view_dashboard(analysis_id: int):
    result = get_analysis_by_id(analysis_id)
    if not result:
        flash("Resume analysis record not found.", "warning")
        return redirect(url_for("index"))

    roles = list(JOB_ROLES.keys())
    return render_template("dashboard.html", result=result, analysis_id=analysis_id, roles=roles)

@app.route("/api/recalculate", methods=["POST"])
def recalculate():
    """Dynamically re-evaluate an existing parsed resume against a new target role."""
    data = request.get_json()
    analysis_id = data.get("analysis_id")
    new_role = data.get("target_role")

    current_data = get_analysis_by_id(analysis_id)
    if not current_data:
        return jsonify({"error": "Analysis not found"}), 404

    parsed_data = current_data["parsed"]
    updated_result = analyzer.analyze(parsed_data, new_role)
    new_id = save_analysis(updated_result)

    return jsonify({
        "status": "success",
        "new_analysis_id": new_id,
        "ats": updated_result["ats"],
        "feedback": updated_result["feedback"]
    })

@app.route("/history")
def history():
    records = get_recent_analyses(50)
    return render_template("history.html", records=records)

@app.route("/export_pdf/<int:analysis_id>")
def export_pdf(analysis_id: int):
    """Generates an ATS Audit & Resume Analysis PDF Report."""
    result = get_analysis_by_id(analysis_id)
    if not result:
        return "Record not found", 404

    parsed = result["parsed"]
    scoring = result["scoring"]
    ats = result["ats"]
    feedback = result["feedback"]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=14
    )
    heading_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#334155")
    )
    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=15,
        spaceAfter=4
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("Smart Resume Analyzer - AI Feedback Report", title_style))
    elements.append(Paragraph(f"SkillOrbit Capstone Evaluation | Candidate: <b>{parsed.get('candidate_name', 'Candidate')}</b> | Target Role: <b>{ats.get('role_title')}</b>", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#6366f1"), spaceAfter=14))

    # Summary Score Table
    score_data = [
        ["Evaluation Metric", "Score Achieved", "Status / Benchmark"],
        ["Overall Resume Score", f"{scoring['total_score']} / 100", scoring['rating']],
        ["ATS Keyword Match Rate", f"{ats['ats_score']}%", f"{ats['total_matched']} of {ats['total_required']} Core Skills Matched"],
        ["Word Count & Brevity", f"{parsed['word_count']} words", "Standard Length" if 250 <= parsed['word_count'] <= 850 else "Review Length"],
        ["Candidate Contact Email", parsed['contact'].get('email') or 'Not Found', "Verified" if parsed['contact'].get('email') else "Missing"],
        ["LinkedIn / GitHub Links", "Present" if parsed['contact'].get('linkedin') or parsed['contact'].get('github') else "Missing", "Profile Optimization"]
    ]

    table = Table(score_data, colWidths=[180, 130, 230])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 14))

    # Matched vs Missing Skills Table
    elements.append(Paragraph("ATS Keyword & Skill Gap Analysis", heading_style))
    matched_str = ", ".join(ats["matched_core"] + ats["matched_secondary"]).title() if (ats["matched_core"] or ats["matched_secondary"]) else "None detected"
    missing_str = ", ".join(ats["missing_core"] + ats["missing_secondary"]).title() if (ats["missing_core"] or ats["missing_secondary"]) else "All target skills detected!"

    skill_matrix = [
        ["Category", "Keywords"],
        ["Matched Skills (Found in Resume)", Paragraph(matched_str, body_style)],
        ["Missing High-Priority Skills", Paragraph(missing_str, body_style)]
    ]
    matrix_table = Table(skill_matrix, colWidths=[160, 380])
    matrix_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#334155")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(matrix_table)
    elements.append(Spacer(1, 14))

    # Recommendations & Feedback
    elements.append(Paragraph("Personalized AI Improvement Suggestions", heading_style))
    for fb in feedback:
        priority_tag = f"<b>[{fb['priority']} Priority - {fb['category']}]</b> "
        elements.append(Paragraph(f"• {priority_tag} <b>{fb['title']}</b>: {fb['description']}", bullet_style))

    # Footer note
    elements.append(Spacer(1, 16))
    elements.append(Paragraph("<i>Generated automatically by SkillOrbit Smart Resume Analyzer AI Capstone Platform.</i>", subtitle_style))

    doc.build(elements)
    buffer.seek(0)
    pdf_filename = f"{parsed.get('candidate_name', 'Resume').replace(' ', '_')}_ATS_Report.pdf"
    return send_file(buffer, as_attachment=True, download_name=pdf_filename, mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
