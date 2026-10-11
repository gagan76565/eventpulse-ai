import unittest

from utils.preprocessing import clean_text
from utils.sentiment import analyze_sentiment
from utils.topic_extraction import extract_topics
from utils.complaint_detector import detect_complaints
from utils.suggestion_engine import generate_suggestions


class FeedbackAnalysisTests(unittest.TestCase):
    def test_clean_text_normalizes_case_and_urls(self):
        self.assertEqual(
            clean_text("Great EVENT! https://example.com"),
            "great event",
        )

    def test_topic_extraction_handles_empty_and_unusable_text(self):
        self.assertEqual(extract_topics([]), [])
        self.assertEqual(extract_topics(["!!!", "the and is"]), [])

    def test_topic_extraction_returns_term_counts(self):
        topics = extract_topics(["great speaker", "great speaker", "good food"])
        self.assertTrue(topics)
        self.assertIn(("great", 2), topics)

    def test_sentiment_counts_cover_all_responses(self):
        feedback = [
            "The event was amazing and excellent",
            "The audio was terrible and disappointing",
            "The event happened today",
        ]
        result = analyze_sentiment(feedback)
        self.assertEqual(
            result["positive"] + result["negative"] + result["neutral"],
            len(feedback),
        )
        self.assertEqual(len(result["results"]), len(feedback))

    def test_complaint_detection_preserves_text_and_deduplicates(self):
        feedback = [
            "Registration was too slow",
            "Registration was too slow",
            "The speakers were excellent",
        ]
        complaints = detect_complaints(feedback)
        self.assertEqual(complaints, ["Registration was too slow"])

    def test_suggestions_are_limited_to_five(self):
        topics = [
            ("audio", 4), ("food", 3), ("venue", 3),
            ("registration", 2), ("networking", 2), ("workshop", 1),
        ]
        suggestions = generate_suggestions(topics, ["slow"] * 3)
        self.assertLessEqual(len(suggestions), 5)
        self.assertTrue(suggestions)


if __name__ == "__main__":
    unittest.main()
