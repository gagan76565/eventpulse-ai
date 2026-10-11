import unittest

from utils.complaint_detector import detect_complaints


class ComplaintDetectorTests(unittest.TestCase):
    def test_positive_feedback_is_not_listed_as_a_complaint(self):
        positive = (
            "best tech conference of the year the hands-on coding labs were worth "
            "the ticket price alone seamless registration process and the digital "
            "badges made connecting on linkedin super easy"
        )
        self.assertEqual(detect_complaints([positive]), [])

    def test_mixed_feedback_returns_the_critical_clause_not_the_praise(self):
        mixed = (
            "great networking opportunities this year i loved how interactive "
            "the workshops were though the event app kept crashing when i tried "
            "to view my personalized schedule please fix the software for next year"
        )
        self.assertEqual(
            detect_complaints([mixed]),
            [
                "the event app kept crashing when i tried to view my personalized "
                "schedule please fix the software for next year"
            ],
        )

    def test_mixed_feedback_without_punctuation_is_trimmed_to_complaint(self):
        mixed = (
            "great networking opportunities this year i loved how interactive "
            "the workshops were the event app kept crashing when i tried to view "
            "my personalized schedule"
        )
        self.assertEqual(
            detect_complaints([mixed]),
            ["the event app kept crashing when i tried to view my personalized schedule"],
        )

    def test_negative_feedback_is_still_detected(self):
        negative = (
            "a total logistical disaster there was no clear signage for the "
            "breakout rooms and the main parking lot was full an hour before "
            "the opening remarks"
        )
        complaints = detect_complaints([negative])
        self.assertEqual(len(complaints), 1)
        self.assertIn("disaster", complaints[0])

    def test_mixed_keynote_review_is_split_at_contrast_marker(self):
        mixed = (
            "the keynote speaker was absolutely phenomenal however the venue "
            "was freezing and the lunch lines were incredibly long"
        )
        complaints = detect_complaints([mixed])
        self.assertEqual(len(complaints), 1)
        self.assertIn("freezing", complaints[0])
        self.assertNotIn("phenomenal", complaints[0])


if __name__ == "__main__":
    unittest.main()
