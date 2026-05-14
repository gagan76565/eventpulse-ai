from collections import Counter


def extract_insights(sentiment_results):

    complaints = []

    positives = []

    for item in sentiment_results:

        if item["sentiment"] == "Negative":

            complaints.append(item["text"])

        elif item["sentiment"] == "Positive":

            positives.append(item["text"])

    common_complaints = Counter(
        complaints
    ).most_common(5)

    common_positives = Counter(
        positives
    ).most_common(5)

    complaint_list = [
        item[0] for item in common_complaints
    ]

    positive_list = [
        item[0] for item in common_positives
    ]

    return complaint_list, positive_list