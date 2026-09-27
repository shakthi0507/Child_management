import unittest
from datetime import date

from app.services.assessment_availability import age_group_applies, age_in_completed_months


class AssessmentAvailabilityTests(unittest.TestCase):
    def test_calendar_age_counts_completed_months(self):
        self.assertEqual(age_in_completed_months(date(2024, 5, 20), date(2026, 9, 19)), 27)
        self.assertEqual(age_in_completed_months(date(2024, 5, 20), date(2026, 9, 20)), 28)
        self.assertEqual(age_in_completed_months(date(2024, 5, 21), date(2026, 9, 20)), 27)
        self.assertIsNone(age_in_completed_months(None, date(2026, 9, 20)))
        self.assertIsNone(age_in_completed_months(date(2027, 1, 1), date(2026, 9, 20)))

    def test_range_exact_month_and_invalid_labels(self):
        self.assertTrue(age_group_applies("24-36", 24))
        self.assertTrue(age_group_applies("24-36", 36))
        self.assertFalse(age_group_applies("24-36", 37))
        self.assertTrue(age_group_applies("24 months", 24))
        self.assertFalse(age_group_applies("24 months", 25))
        self.assertFalse(age_group_applies("unknown", 24))
        self.assertFalse(age_group_applies(None, 24))
        self.assertFalse(age_group_applies("24-36", None))


if __name__ == "__main__":
    unittest.main()
