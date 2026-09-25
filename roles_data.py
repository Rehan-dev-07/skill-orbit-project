"""
Role profiles, skills taxonomy, and industry keywords for ATS evaluation.
Covers core tech tracks: Data Analyst, Web Developer, AI Engineer, Cloud Engineer,
Software Engineer, DevOps Engineer, Full Stack Developer, and Cybersecurity Analyst.
"""

JOB_ROLES = {
    "AI Engineer": {
        "title": "Artificial Intelligence / Machine Learning Engineer",
        "category": "Artificial Intelligence & Data Science",
        "description": "Designs, builds, and deploys intelligent models and algorithms.",
        "core_skills": [
            "python", "machine learning", "deep learning", "nlp", "computer vision",
            "pytorch", "tensorflow", "scikit-learn", "data preprocessing", "model evaluation"
        ],
        "secondary_skills": [
            "pandas", "numpy", "transformers", "hugging face", "opencv", "sql",
            "docker", "fastapi", "flask", "git", "cloud computing", "llm", "genai"
        ],
        "recommended_certifications": [
            "TensorFlow Developer Certificate",
            "AWS Certified Machine Learning - Specialty",
            "DeepLearning.AI Machine Learning Specialization",
            "Google Professional Machine Learning Engineer"
        ],
        "essential_sections": ["Summary", "Technical Skills", "Projects", "Experience", "Education"],
        "action_verbs": ["trained", "optimized", "fine-tuned", "deployed", "evaluated", "architected", "implemented"]
    },
    "Data Analyst": {
        "title": "Data Analyst / Business Intelligence Specialist",
        "category": "Data & Analytics",
        "description": "Translates complex datasets into actionable business insights.",
        "core_skills": [
            "sql", "python", "excel", "tableau", "power bi", "data visualization",
            "exploratory data analysis", "statistical analysis", "data cleaning"
        ],
        "secondary_skills": [
            "r", "pandas", "numpy", "matplotlib", "seaborn", "business intelligence",
            "etl", "mysql", "postgresql", "bigquery", "storytelling", "metrics", "kpi"
        ],
        "recommended_certifications": [
            "Google Data Analytics Professional Certificate",
            "Microsoft Certified: Power BI Data Analyst Associate",
            "Tableau Desktop Specialist",
            "IBM Data Analyst Professional Certificate"
        ],
        "essential_sections": ["Summary", "Skills", "Projects", "Experience", "Education"],
        "action_verbs": ["analyzed", "visualized", "extracted", "modeled", "uncovered", "automated", "reported"]
    },
    "Web Developer": {
        "title": "Web Developer (Frontend / UI Engineer)",
        "category": "Software & Web Development",
        "description": "Builds responsive, high-performance web applications and user interfaces.",
        "core_skills": [
            "javascript", "html5", "css3", "react", "responsive design",
            "typescript", "git", "web performance", "dom manipulation"
        ],
        "secondary_skills": [
            "vue", "angular", "next.js", "tailwind css", "bootstrap", "sass",
            "rest api", "json", "webpack", "vite", "testing", "ui/ux", "cross-browser"
        ],
        "recommended_certifications": [
            "Meta Front-End Developer Professional Certificate",
            "freeCodeCamp Responsive Web Design Certificate",
            "Certified Web Professional (CWP)"
        ],
        "essential_sections": ["Summary", "Technical Skills", "Projects", "Experience", "Education"],
        "action_verbs": ["developed", "engineered", "designed", "integrated", "optimized", "refactored", "built"]
    },
    "Cloud Engineer": {
        "title": "Cloud Solutions & Infrastructure Engineer",
        "category": "Cloud & Infrastructure",
        "description": "Architects, provisions, and scales reliable cloud environments.",
        "core_skills": [
            "aws", "azure", "google cloud", "docker", "kubernetes",
            "terraform", "linux", "ci/cd", "cloud architecture", "networking"
        ],
        "secondary_skills": [
            "python", "bash", "ansible", "iam", "cloudwatch", "vpc",
            "microservices", "infrastructure as code", "git", "monitoring", "serverless"
        ],
        "recommended_certifications": [
            "AWS Certified Solutions Architect – Associate",
            "Microsoft Certified: Azure Administrator Associate",
            "Google Cloud Associate Cloud Engineer",
            "HashiCorp Certified: Terraform Associate"
        ],
        "essential_sections": ["Summary", "Skills", "Experience", "Projects", "Certifications", "Education"],
        "action_verbs": ["migrated", "automated", "provisioned", "architected", "monitored", "scaled", "secured"]
    },
    "Software Engineer": {
        "title": "Software Development Engineer (SDE)",
        "category": "Software Engineering",
        "description": "Designs and develops robust backend systems, APIs, and scalable software.",
        "core_skills": [
            "python", "java", "c++", "data structures", "algorithms",
            "object-oriented programming", "git", "sql", "rest api"
        ],
        "secondary_skills": [
            "system design", "spring boot", "django", "fastapi", "docker",
            "unit testing", "postgresql", "redis", "concurrency", "design patterns"
        ],
        "recommended_certifications": [
            "Oracle Certified Professional: Java SE Developer",
            "AWS Certified Developer - Associate",
            "Meta Back-End Developer Professional Certificate"
        ],
        "essential_sections": ["Summary", "Technical Skills", "Projects", "Experience", "Education"],
        "action_verbs": ["implemented", "architected", "designed", "scaled", "debugged", "optimized", "maintained"]
    },
    "DevOps Engineer": {
        "title": "DevOps & Site Reliability Engineer",
        "category": "DevOps & SRE",
        "description": "Streamlines continuous deployment, automated testing, and reliability.",
        "core_skills": [
            "docker", "kubernetes", "ci/cd", "jenkins", "git",
            "linux", "bash", "terraform", "monitoring", "prometheus"
        ],
        "secondary_skills": [
            "python", "grafana", "ansible", "aws", "helm", "github actions",
            "yaml", "site reliability", "logging", "elk stack", "incident management"
        ],
        "recommended_certifications": [
            "Certified Kubernetes Administrator (CKA)",
            "AWS Certified DevOps Engineer - Professional",
            "Docker Certified Associate (DCA)"
        ],
        "essential_sections": ["Summary", "Technical Skills", "Experience", "Projects", "Certifications", "Education"],
        "action_verbs": ["orchestrated", "automated", "deployed", "configured", "monitored", "streamlined", "secured"]
    }
}

STANDARD_SECTIONS = [
    "summary", "objective", "profile", "about",
    "education", "academic", "qualifications",
    "experience", "work history", "employment", "internship",
    "skills", "technical skills", "competencies", "expertise",
    "projects", "academic projects", "key projects",
    "certifications", "licenses", "awards", "achievements",
    "contact", "contact information"
]
