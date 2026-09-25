"""
Unit tests for the Resume Parser, Analyzer, and SQLite Database.
"""

import os
import unittest
from parser import ResumeParser
from analyzer import ResumeAnalyzer
from models import init_db, save_analysis, get_recent_analyses, get_analysis_by_id

class TestResumeAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.parser = ResumeParser()
        cls.analyzer = ResumeAnalyzer()
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.sample_ai_pdf = os.path.join(cls.base_dir, "sample_resumes", "sample_ai_engineer.pdf")
        cls.sample_ai_docx = os.path.join(cls.base_dir, "sample_resumes", "sample_ai_engineer.docx")

    def test_pdf_parsing(self):
        self.assertTrue(os.path.exists(self.sample_ai_pdf), "Sample PDF should exist")
        data = self.parser.parse(self.sample_ai_pdf)
        self.assertIn("arjun.sharma.ai@gmail.com", data["contact"]["email"])
        self.assertGreater(data["word_count"], 100)
        self.assertTrue(data["sections"]["skills"])
        self.assertTrue(data["sections"]["projects"])

    def test_docx_parsing(self):
        self.assertTrue(os.path.exists(self.sample_ai_docx), "Sample DOCX should exist")
        data = self.parser.parse(self.sample_ai_docx)
        self.assertIn("arjun.sharma.ai@gmail.com", data["contact"]["email"])
        self.assertGreater(data["word_count"], 100)

    def test_analyzer_scoring(self):
        data = self.parser.parse(self.sample_ai_pdf)
        result = self.analyzer.analyze(data, "AI Engineer")
        
        # Verify score bounds
        total_score = result["scoring"]["total_score"]
        self.assertGreaterEqual(total_score, 0)
        self.assertLessEqual(total_score, 100)
        self.assertGreater(total_score, 70, "Strong sample resume should score well")

        # Verify ATS scoring
        ats_score = result["ats"]["ats_score"]
        self.assertGreaterEqual(ats_score, 50)
        self.assertIn("python", [s.lower() for s in result["ats"]["matched_core"]])

        # Verify feedback presence
        self.assertGreater(len(result["feedback"]), 0)

    def test_database_persistence(self):
        data = self.parser.parse(self.sample_ai_pdf)
        result = self.analyzer.analyze(data, "AI Engineer")
        rec_id = save_analysis(result)
        self.assertIsInstance(rec_id, int)

        fetched = get_analysis_by_id(rec_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["parsed"]["contact"]["email"], "arjun.sharma.ai@gmail.com")

if __name__ == "__main__":
    unittest.main()
