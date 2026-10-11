from __future__ import annotations

import re
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer


def extract_topics(feedback_list, top_n=10):
    """Return frequent terms/phrases as (label, count) pairs.

    Empty or punctuation-only batches are valid input and return an empty list.
    """
    texts = [
        re.sub(r"\s+", " ", str(text)).strip()
        for text in (feedback_list or [])
        if str(text).strip()
    ]
    if not texts:
        return []

    vectorizer = CountVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=1000,
        token_pattern=r"(?u)\b\w\w+\b",
    )
    try:
        matrix = vectorizer.fit_transform(texts)
    except ValueError as exc:
        if "empty vocabulary" in str(exc).lower() or "no terms remain" in str(exc).lower():
            return []
        raise

    terms = vectorizer.get_feature_names_out()
    counts = matrix.sum(axis=0).A1
    frequencies = Counter({
        str(term): int(count)
        for term, count in zip(terms, counts)
        if int(count) > 0
    })
    return frequencies.most_common(max(0, int(top_n)))
