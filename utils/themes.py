from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

import numpy as np


def extract_themes(cleaned_feedback):

    if len(cleaned_feedback) < 2:
        return cleaned_feedback

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=100
    )

    X = vectorizer.fit_transform(cleaned_feedback)

    n_clusters = min(5, len(cleaned_feedback))

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    model.fit(X)

    feature_names = vectorizer.get_feature_names_out()

    themes = []

    for cluster_center in model.cluster_centers_:

        top_index = np.argmax(cluster_center)

        theme = feature_names[top_index]

        if theme not in themes:
            themes.append(theme)

    return themes[:10]