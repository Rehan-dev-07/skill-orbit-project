# SkillOrbit AI Capstone Project: Smart Resume Analyzer with AI-Based Feedback

## 📌 Project Overview
The **Smart Resume Analyzer with AI-Based Feedback** is an artificial intelligence and natural language processing web platform built to simulate real-world Applicant Tracking Systems (ATS) used by top tech recruiters and HR platforms.

The application allows students and job-seekers to upload resumes in multiple formats (PDF, DOCX, TXT), extracts structural and contact metadata, evaluates resumes across 6 key scoring dimensions (producing a score out of 100), performs target-role ATS keyword matching, and generates prioritized, actionable feedback to bridge skill gaps.

---

## 🛠️ Technology Stack
- **Backend**: Python 3.11, Flask
- **Document Processing**: `pypdf` (PDF extraction), `python-docx` (DOCX parsing)
- **AI & NLP Logic**: Regular expressions, tokenizers, n-gram matching, heuristic scoring models
- **Database**: SQLite (`resumes.db`) with full JSON audit logs
- **Frontend**: HTML5, Vanilla CSS3 (Modern Glassmorphic design system), Bootstrap 5, FontAwesome 6
- **Data Visualization**: Chart.js (Radial Score Meters, 6-Parameter Bar Charts, Keyword Donut Charts)
- **Report Generation**: ReportLab (Automated multi-page PDF generation)
- **Presentation**: `python-pptx` (Widescreen 16:9 slides)

---

## 🏗️ 5 Core Capstone Modules

### Module 1: Resume Upload & Parsing
- Multi-format ingestion supporting PDF, DOCX, and TXT files.
- Automated extraction of candidate name, email, phone number, LinkedIn URL, GitHub profile, and portfolio links.
- Detection of standard resume sections (Summary, Education, Experience, Skills, Projects, Certifications).

### Module 2: Resume Score Analyzer
Calculates an objective score out of 100 based on 6 weighted parameters:
1. **Contact Information (15 pts)**: Email, phone, verified professional links (LinkedIn & GitHub).
2. **Resume Structure & Formatting (20 pts)**: Section balance and optimal word count (250–850 words).
3. **Technical Skills Section (20 pts)**: Dedicated skill headings and density of industry-standard tools.
4. **Experience & Internships (15 pts)**: Action verbs (engineered, deployed, optimized, analyzed).
5. **Projects Section (15 pts)**: Real-world projects, tech stacks, and quantifiable impact metrics.
6. **Education & Completeness (15 pts)**: Academic degree, graduation details, and recognized certifications.

### Module 3: ATS Keyword Checker
- Compares extracted text against industry taxonomies for targeted tech tracks:
  - **AI Engineer** (PyTorch, TensorFlow, Machine Learning, Deep Learning, NLP, Computer Vision, Docker, FastAPI)
  - **Data Analyst** (SQL, Python, Tableau, Power BI, Excel, ETL, Exploratory Data Analysis)
  - **Web Developer** (React, TypeScript, JavaScript, HTML5, CSS3, REST API, Git, Vite)
  - **Cloud Engineer** (AWS, Azure, Docker, Kubernetes, Terraform, Linux, CI/CD)
  - **Software Engineer** (Data Structures, Algorithms, OOP, Java, Python, System Design)
  - **DevOps Engineer** (Kubernetes, Docker, Jenkins, Terraform, Prometheus, CI/CD)
- Weighted match computation (Core Skills 70% + Supporting Skills 30%).
- Real-time role switcher without re-uploading documents.

### Module 4: Smart Feedback System
- Actionable advice categorized by urgency:
  - **High Priority (Critical)**: Missing core role competencies, absent projects section, extreme brevity.
  - **Medium Priority**: Quantifying accomplishments using the XYZ formula (Accomplished [X] measured by [Y] by doing [Z]), adding GitHub repositories.
  - **Low Priority**: Recommended industry certifications and formatting enhancements.

### Module 5: Dashboard and Report Generation
- Sleek glassmorphic web dashboard with responsive layout.
- Real-time Chart.js radial progress meters and breakdown graphs.
- Direct PDF report download (`/export_pdf/<id>`).
- Scan history page with persistent SQLite storage.

---

## 🚀 Local Installation & Setup

1. **Clone or Navigate to the Repository**:
   ```bash
   cd "c:\Users\ishan\Desktop\skill orbit project"
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Unit Tests**:
   ```bash
   python -m unittest tests/test_analyzer.py
   ```

4. **Launch the Flask Web Application**:
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://localhost:5000`.

---

## ☁️ Deployment Instructions

### Option 1: Deploy to Render
1. Push project to your GitHub repository.
2. Log in to [Render](https://render.com) and click **New + > Web Service**.
3. Select your repository.
4. Set:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (or `python app.py`)
5. Click **Deploy Web Service**.

### Option 2: Deploy to Vercel / Railway
- Configured via `vercel.json` or `Procfile` for one-click deployment.

---

## 📁 Repository File Tree
```
├── app.py                     # Main Flask Application & API routes
├── analyzer.py                # Scoring, ATS matching, and smart feedback engine
├── parser.py                  # Multi-format document text & metadata extractor
├── models.py                  # SQLite database models & query handlers
├── roles_data.py              # Industry-standard skill taxonomies and keywords
├── generate_presentation.py   # Automated PowerPoint presentation generator
├── generate_report.py         # Automated PDF Capstone Report generator
├── requirements.txt           # Python dependencies
├── Procfile                   # Cloud process execution command
├── render.yaml                # Render Blueprint deployment definition
├── sample_resumes/            # Sample test resumes in TXT, DOCX, and PDF formats
│   ├── sample_ai_engineer.pdf
│   ├── sample_ai_engineer.docx
│   ├── sample_data_analyst.pdf
│   └── sample_web_developer.pdf
├── static/                    # Glassmorphism CSS and Chart.js frontend controller
│   ├── css/style.css
│   └── js/main.js
├── templates/                 # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   └── history.html
├── tests/                     # Automated unit test suite
│   └── test_analyzer.py
└── deliverables/              # Official SkillOrbit submission package
    ├── Smart_Resume_Analyzer_Report.pdf
    ├── Smart_Resume_Analyzer_Presentation.pptx
    ├── PROJECT_DOCUMENTATION.md
    └── SUBMISSION_INSTRUCTIONS.md
```
