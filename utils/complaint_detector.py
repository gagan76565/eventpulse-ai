NEGATIVE_KEYWORDS = [
    'bad',
    'poor',
    'low',
    'crowded',
    'slow',
    'terrible',
    'boring',
    'confusing',
    'noise',
    'issue',
    'problem'
]


def detect_complaints(feedback_list):

    complaints = []

    for feedback in feedback_list:

        text = feedback.lower()

        for word in NEGATIVE_KEYWORDS:

            if word in text:
                complaints.append(feedback)
                break

    return complaints