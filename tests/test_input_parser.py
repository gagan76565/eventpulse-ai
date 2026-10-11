import unittest

from utils.input_parser import split_feedback


class FeedbackInputParserTests(unittest.TestCase):
    def test_plain_text_still_counts_one_nonempty_line_per_response(self):
        self.assertEqual(
            split_feedback("Great speakers\n\nPoor audio\n Smooth registration "),
            ["Great speakers", "Poor audio", "Smooth registration"],
        )

    def test_structured_attendee_blocks_only_extract_feedback_fields(self):
        pasted = """- **Attendee ID:** 101
  - **Rating:** ⭐⭐⭐⭐⭐ (5/5)
  - **Feedback:** "The keynote was excellent, but lunch lines were long."
- **Attendee ID:** 102
  - **Rating:** ⭐⭐ (2/5)
  - **Feedback:** "The audio was terrible." """
        self.assertEqual(
            split_feedback(pasted),
            [
                "The keynote was excellent, but lunch lines were long.",
                "The audio was terrible.",
            ],
        )

    def test_empty_text_returns_empty_list(self):
        self.assertEqual(split_feedback("  \n  "), [])

    def test_unlabeled_bullets_remain_separate_responses(self):
        self.assertEqual(
            split_feedback("- Great event\n- Poor food"),
            ["- Great event", "- Poor food"],
        )


if __name__ == "__main__":
    unittest.main()
