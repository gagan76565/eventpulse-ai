from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(feedback_list):

    results = []

    positive = 0
    negative = 0
    neutral = 0

    for feedback in feedback_list:

        score = analyzer.polarity_scores(feedback)

        compound = score["compound"]

        if compound >= 0.05:

            sentiment = "Positive"
            positive += 1

        elif compound <= -0.05:

            sentiment = "Negative"
            negative += 1

        else:

            sentiment = "Neutral"
            neutral += 1

        results.append({
            "text": feedback,
            "sentiment": sentiment,
            "score": compound
        })

    total = len(feedback_list)

    sentiment_summary = {

        "positive_percent":
            round((positive / total) * 100),

        "negative_percent":
            round((negative / total) * 100),

        "neutral_percent":
            round((neutral / total) * 100)
    }

    return results, sentiment_summary