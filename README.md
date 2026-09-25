# 🎯 Smart Resume Analyzer with AI-Based Feedback
### SkillOrbit Artificial Intelligence Capstone Project

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Completed-success)

A full-stack, AI-powered recruitment technology platform that helps students and job applicants evaluate, optimize, and tailor their resumes according to industry Applicant Tracking System (ATS) hiring benchmarks.

---

## 🌟 Key Features
- **Module 1: Multi-Format Upload & Parsing**: Supports `.pdf`, `.docx`, and `.txt` documents; extracts candidate contact information (email, phone, LinkedIn, GitHub) and identifies resume sections.
- **Module 2: Resume Score Analyzer**: Objective 100-point scoring algorithm evaluating Structure, Skills, Experience, Projects, Education, and Contact completeness.
- **Module 3: ATS Keyword Checker**: Compares resume text against role taxonomies (AI Engineer, Data Analyst, Web Developer, Cloud Engineer, Software Engineer, DevOps) with weighted keyword scoring.
- **Module 4: Smart Feedback System**: Categorized, prioritized (High, Medium, Low) actionable recommendations utilizing the XYZ achievement formula.
- **Module 5: Interactive Dashboard & PDF Audit**: Glassmorphism UI, real-time Chart.js radial progress meters, instant dynamic role switcher via AJAX, and one-click PDF audit export.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+ (Python 3.11 recommended)
- `pip` package manager

### 2. Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd "skill orbit project"

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
python -m unittest tests/test_analyzer.py
```

### 4. Start the Application
```bash
python app.py
```
Open your web browser and visit: `http://localhost:5000`

---

## 📦 Project Deliverables
All required deliverables for SkillOrbit submission are ready in `deliverables/`:
- 📄 **Project Report PDF**: [`deliverables/Smart_Resume_Analyzer_Report.pdf`](deliverables/Smart_Resume_Analyzer_Report.pdf)
- 📊 **PowerPoint Presentation**: [`deliverables/Smart_Resume_Analyzer_Presentation.pptx`](deliverables/Smart_Resume_Analyzer_Presentation.pptx)
- 📝 **Technical Documentation**: [`deliverables/PROJECT_DOCUMENTATION.md`](deliverables/PROJECT_DOCUMENTATION.md)
- 🎬 **Demo Video Walkthrough Script**: [`DEMO_WALKTHROUGH_SCRIPT.md`](DEMO_WALKTHROUGH_SCRIPT.md)
- 🔗 **Google Form Submission Instructions**: [`deliverables/SUBMISSION_INSTRUCTIONS.md`](deliverables/SUBMISSION_INSTRUCTIONS.md)

---

## ☁️ Deployment
Ready for 1-click deployment on **Render**, **Railway**, or **Vercel** with included `Procfile`, `render.yaml`, and `runtime.txt`.
