import unittest
from pathlib import Path

from app.database.import_assessment_docx import parse_questions


class AssessmentDocumentImportTests(unittest.TestCase):
    def test_ldst_ages_domains_and_examples_are_parsed(self):
        source = Path(__file__).with_name("001 Assessment - initial.docx")
        assessments = parse_questions(source)

        self.assertEqual(
            sorted(assessments),
            [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36],
        )
        self.assertEqual(sum(map(len, assessments.values())), 389)

        first = next(
            item
            for item in assessments[3]
            if item["code"] == "GM3-01"
        )
        self.assertIn("Example:", first["text"])
        self.assertEqual(first["domain"], "Gross Motor")

        domains = {item["domain"] for items in assessments.values() for item in items}
        self.assertEqual(
            domains,
            {
                "Gross Motor",
                "Fine Motor",
                "Speech & Language",
                "Cognition",
                "Social & Emotional",
                "Adaptive / Self-Help",
            },
        )


if __name__ == "__main__":
    unittest.main()
