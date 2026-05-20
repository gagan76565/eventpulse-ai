from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter


def extract_topics(feedback_list, top_n=10):

    vectorizer = CountVectorizer(
        stop_words='english',
        ngram_range=(1, 2)
    )

    X = vectorizer.fit_transform(feedback_list)

    words = vectorizer.get_feature_names_out()

    counts = X.sum(axis=0).A1

    word_freq = list(zip(words, counts))

    sorted_words = sorted(
        word_freq,
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_words[:top_n]