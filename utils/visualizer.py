import matplotlib
matplotlib.use("Agg")

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import os
import uuid


def generate_wordcloud(feedback_list):

    if not feedback_list:
        return None

    combined_text = " ".join(feedback_list)

    filename = f"{uuid.uuid4().hex}.png"

    output_folder = "static/images"

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(
        output_folder,
        filename
    )

    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white"
    ).generate(combined_text)

    plt.figure(figsize=(10, 5))

    plt.imshow(wordcloud, interpolation="bilinear")

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()

    return filename