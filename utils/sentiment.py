from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(feedback_list):

    results = []

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for feedback in feedback_list:

        score = analyzer.polarity_scores(feedback)

        compound = score['compound']

        if compound >= 0.05:
            sentiment = 'Positive'
            positive_count += 1

        elif compound <= -0.05:
            sentiment = 'Negative'
            negative_count += 1

        else:
            sentiment = 'Neutral'
            neutral_count += 1

        results.append({
            'text': feedback,
            'sentiment': sentiment,
            'score': compound
        })

    return {
        'results': results,
        'positive': positive_count,
        'negative': negative_count,
        'neutral': neutral_count
    }