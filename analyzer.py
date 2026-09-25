"""
Modules 2, 3 & 4: Resume Scoring, ATS Keyword Checker, and Smart Feedback System.
Evaluates resume quality, computes ATS compatibility for chosen roles,
and generates smart, prioritized improvement suggestions.
"""

import re
from typing import Dict, Any, List, Tuple
from roles_data import JOB_ROLES

class ResumeAnalyzer:
    def __init__(self):
        self.roles = JOB_ROLES

    def calculate_resume_score(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Module 2: Evaluates 6 core dimensions:
        1. Contact Information (15 pts)
        2. Resume Structure & Headings (20 pts)
        3. Skills Section (20 pts)
        4. Experience & Internships (15 pts)
        5. Projects Section (15 pts)
        6. Education & Completeness (15 pts)
        Total: 100 points
        """
        text = parsed_data["text"].lower()
        contact = parsed_data["contact"]
        sections = parsed_data["sections"]
        word_count = parsed_data["word_count"]

        breakdown = {}
        deductions = []
        strengths = []

        # 1. Contact Information (Max 15)
        contact_score = 0
        if contact.get("email"):
            contact_score += 5
            strengths.append("Valid professional email detected.")
        else:
            deductions.append("Missing email address in contact section.")

        if contact.get("phone"):
            contact_score += 4
            strengths.append("Contact telephone number found.")
        else:
            deductions.append("Missing phone number.")

        if contact.get("linkedin"):
            contact_score += 3
            strengths.append("LinkedIn profile link present.")
        else:
            deductions.append("Add your customized LinkedIn profile URL.")

        if contact.get("github") or "portfolio" in text or "github.com" in text:
            contact_score += 3
            strengths.append("GitHub / Portfolio link detected.")
        else:
            deductions.append("Include a GitHub or portfolio link to showcase repositories.")

        breakdown["contact_score"] = min(15, contact_score)

        # 2. Resume Structure (Max 20)
        structure_score = 0
        detected_sections_count = sum(1 for v in sections.values() if v)
        structure_score += min(15, detected_sections_count * 2.5)

        # Formatting / Length checks
        if 250 <= word_count <= 850:
            structure_score += 5
            strengths.append(f"Ideal resume length ({word_count} words, approx 1-2 pages).")
        elif word_count < 250:
            structure_score += 2
            deductions.append(f"Resume is too brief ({word_count} words). Expand with bullet points.")
        else:
            structure_score += 3
            deductions.append(f"Resume is lengthy ({word_count} words). Consider condensing to 1-2 pages.")

        breakdown["structure_score"] = round(min(20, structure_score), 1)

        # 3. Skills Section (Max 20)
        skills_score = 0
        if sections.get("skills"):
            skills_score += 8
        else:
            deductions.append("No explicit 'Skills' or 'Technical Skills' heading found.")

        # Count total tech terms across text
        tech_words = ["python", "java", "sql", "html", "css", "javascript", "react", "c++", "git", "docker", "aws", "data", "api", "linux"]
        found_tech = [w for w in tech_words if re.search(r'\b' + re.escape(w) + r'\b', text)]
        skills_score += min(12, len(found_tech) * 1.5)
        if len(found_tech) >= 5:
            strengths.append(f"Strong variety of technical keywords identified ({len(found_tech)}+ core tools).")
        breakdown["skills_score"] = round(min(20, skills_score), 1)

        # 4. Experience / Internships (Max 15)
        exp_score = 0
        if sections.get("experience") or "internship" in text or "experience" in text:
            exp_score += 8
        # Action verbs check
        action_verbs = ["developed", "built", "designed", "created", "led", "managed", "analyzed", "improved", "implemented", "achieved"]
        found_actions = [v for v in action_verbs if re.search(r'\b' + v + r'\b', text)]
        exp_score += min(7, len(found_actions) * 1.2)
        if len(found_actions) >= 4:
            strengths.append("Active impact verbs used (e.g., implemented, developed, analyzed).")
        else:
            deductions.append("Begin project and work experience bullet points with strong action verbs.")
        breakdown["experience_score"] = round(min(15, exp_score), 1)

        # 5. Projects Section (Max 15)
        proj_score = 0
        if sections.get("projects"):
            proj_score += 8
            strengths.append("Dedicated Projects section highlights practical skills.")
        else:
            deductions.append("Add a dedicated 'Projects' section to showcase real-world development work.")
        # Check for measurable metrics (numbers, %, metrics)
        has_metrics = bool(re.search(r'\b(\d+%\b|\$\d+|\b\d+\s*(users|clients|records|accuracy|reduction|increase|faster)\b)', text))
        if has_metrics:
            proj_score += 7
            strengths.append("Quantifiable impact and metrics demonstrated in project descriptions.")
        else:
            proj_score += 3
            deductions.append("Include quantifiable metrics (e.g., 'improved accuracy by 15%', 'supported 500+ users').")
        breakdown["projects_score"] = round(min(15, proj_score), 1)

        # 6. Education & Completeness (Max 15)
        edu_score = 0
        if sections.get("education"):
            edu_score += 7
            strengths.append("Clear Education credentials listed.")
        else:
            deductions.append("Add an 'Education' section with your degree and graduation year.")

        # Degrees check
        degrees = ["bachelor", "b.tech", "b.e.", "bca", "mca", "master", "m.tech", "b.sc", "computer science", "engineering"]
        if any(d in text for d in degrees):
            edu_score += 4

        # Certifications bonus check
        if sections.get("certifications") or any(k in text for k in ["certified", "certification", "certificate", "coursera", "udemy"]):
            edu_score += 4
            strengths.append("Professional certifications / courses included.")
        else:
            deductions.append("Consider adding recognized certifications to strengthen credentials.")

        breakdown["education_score"] = round(min(15, edu_score), 1)

        total_score = round(sum(breakdown.values()), 1)
        total_score = min(100.0, max(0.0, total_score))

        # Overall rating band
        if total_score >= 85:
            rating = "Excellent (Ready for Tier-1 ATS)"
            badge_class = "success"
        elif total_score >= 70:
            rating = "Good (Competitive with minor polish)"
            badge_class = "primary"
        elif total_score >= 50:
            rating = "Average (Requires Key Section Improvements)"
            badge_class = "warning"
        else:
            rating = "Needs Significant Rework"
            badge_class = "danger"

        return {
            "total_score": total_score,
            "rating": rating,
            "badge_class": badge_class,
            "breakdown": breakdown,
            "strengths": strengths,
            "deductions": deductions
        }

    def analyze_ats_keywords(self, text: str, role_name: str) -> Dict[str, Any]:
        """
        Module 3: Compares resume against industry keywords for a specific role.
        Calculates ATS match percentage, lists matched skills, missing skills, and role tips.
        """
        role_info = self.roles.get(role_name, self.roles["Software Engineer"])
        text_lower = text.lower()

        core_skills = role_info["core_skills"]
        secondary_skills = role_info["secondary_skills"]

        matched_core = []
        missing_core = []
        for skill in core_skills:
            # Word boundary regex matching or multi-word phrase matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                matched_core.append(skill)
            else:
                missing_core.append(skill)

        matched_secondary = []
        missing_secondary = []
        for skill in secondary_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                matched_secondary.append(skill)
            else:
                missing_secondary.append(skill)

        # ATS Match Calculation (Weighted: Core 70%, Secondary 30%)
        core_weight = (len(matched_core) / max(1, len(core_skills))) * 70
        secondary_weight = (len(matched_secondary) / max(1, len(secondary_skills))) * 30
        ats_score = round(core_weight + secondary_weight, 1)
        ats_score = min(100.0, ats_score)

        return {
            "role_name": role_name,
            "role_title": role_info["title"],
            "role_category": role_info["category"],
            "role_description": role_info["description"],
            "ats_score": ats_score,
            "matched_core": matched_core,
            "missing_core": missing_core,
            "matched_secondary": matched_secondary,
            "missing_secondary": missing_secondary,
            "total_matched": len(matched_core) + len(matched_secondary),
            "total_required": len(core_skills) + len(secondary_skills),
            "recommended_certifications": role_info.get("recommended_certifications", []),
            "action_verbs": role_info.get("action_verbs", [])
        }

    def generate_smart_feedback(self, parsed_data: Dict[str, Any], score_data: Dict[str, Any], ats_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Module 4: Generates actionable, categorized suggestions with priority flags.
        """
        suggestions = []
        role_name = ats_data["role_name"]

        # 1. Missing Core Skills (High Priority)
        if ats_data["missing_core"]:
            top_missing = ats_data["missing_core"][:4]
            skills_str = ", ".join(f"'{s.title()}'" for s in top_missing)
            suggestions.append({
                "category": "Target Role Keywords",
                "priority": "High",
                "icon": "fa-bullseye",
                "color": "danger",
                "title": f"Integrate Core {role_name} Technologies",
                "description": f"Recruiters and ATS algorithms screen for {skills_str}. If you have working experience or projects using these, explicitly list them in your Skills section."
            })

        # 2. Projects & Evidence (High / Medium Priority)
        if not parsed_data["sections"].get("projects"):
            suggestions.append({
                "category": "Portfolio & Practical Experience",
                "priority": "High",
                "icon": "fa-diagram-project",
                "color": "danger",
                "title": f"Add 2-3 Featured {role_name} Projects",
                "description": "Create a clear 'Projects' section containing project titles, tech stack utilized, live deployment links, and measurable accomplishments."
            })
        elif ats_data["ats_score"] < 70:
            suggestions.append({
                "category": "Portfolio & Practical Experience",
                "priority": "Medium",
                "icon": "fa-laptop-code",
                "color": "warning",
                "title": "Highlight Role-Aligned Project Deliverables",
                "description": f"Tailor your project descriptions to emphasize {role_name} tools (e.g. {', '.join(ats_data['missing_core'][:2]) if ats_data['missing_core'] else 'modern workflows'})."
            })

        # 3. Contact & Social Presence (Medium Priority)
        contact = parsed_data["contact"]
        if not contact.get("linkedin") or not contact.get("github"):
            missing_links = []
            if not contact.get("linkedin"): missing_links.append("LinkedIn Profile")
            if not contact.get("github"): missing_links.append("GitHub / Portfolio")
            suggestions.append({
                "category": "Contact & Online Footprint",
                "priority": "Medium",
                "icon": "fa-address-card",
                "color": "warning",
                "title": f"Add {' and '.join(missing_links)}",
                "description": "Modern tech recruiters click directly through to verified profiles to inspect code quality and professional recommendations."
            })

        # 4. Resume Formatting & Structure
        if parsed_data["word_count"] < 250:
            suggestions.append({
                "category": "Resume Structure & Content",
                "priority": "High",
                "icon": "fa-file-lines",
                "color": "danger",
                "title": "Expand Resume Breadth (Currently Under 250 Words)",
                "description": "Your resume is brief. Provide 3-4 descriptive bullet points per project and work experience with problem, action, and results."
            })
        elif parsed_data["word_count"] > 800:
            suggestions.append({
                "category": "Resume Formatting",
                "priority": "Medium",
                "icon": "fa-compress",
                "color": "info",
                "title": "Condense Content for Maximum Scannability",
                "description": "At over 800 words, recruiters may lose focus. Use punchy bullet points and remove outdated secondary school coursework."
            })

        # 5. Certifications & Credibility (Low / Medium Priority)
        if not parsed_data["sections"].get("certifications"):
            rec_cert = ats_data.get("recommended_certifications", [])
            cert_names = ", ".join(rec_cert[:2]) if rec_cert else "Industry Recognized Badges"
            suggestions.append({
                "category": "Certifications & Lifelong Learning",
                "priority": "Low",
                "icon": "fa-award",
                "color": "primary",
                "title": "Earn Role-Specific Industry Certifications",
                "description": f"Boost ATS credibility for {role_name} by including certifications such as {cert_names}."
            })

        # 6. Action Verbs & Metrics
        suggestions.append({
            "category": "Bullet Point Impact",
            "priority": "Medium",
            "icon": "fa-chart-line",
            "color": "success",
            "title": "Employ the XYZ Formula (Accomplished [X] measured by [Y] by doing [Z])",
            "description": f"Leverage strong action verbs like {', '.join(ats_data.get('action_verbs', ['engineered', 'deployed', 'optimized'])[:4])} paired with numeric results (e.g., 'accelerated load times by 32%')."
        })

        return suggestions

    def analyze(self, parsed_data: Dict[str, Any], role_name: str = "AI Engineer") -> Dict[str, Any]:
        """Orchestrates comprehensive resume analysis."""
        score_data = self.calculate_resume_score(parsed_data)
        ats_data = self.analyze_ats_keywords(parsed_data["text"], role_name)
        feedback = self.generate_smart_feedback(parsed_data, score_data, ats_data)

        return {
            "parsed": parsed_data,
            "scoring": score_data,
            "ats": ats_data,
            "feedback": feedback,
            "available_roles": list(self.roles.keys())
        }
