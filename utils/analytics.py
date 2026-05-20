from wordcloud import WordCloud
import matplotlib.pyplot as plt


def generate_sentiment_chart_data(positive, negative, neutral):

    return {
        'labels': ['Positive', 'Negative', 'Neutral'],
        'values': [
            int(positive),
            int(negative),
            int(neutral)
        ]
    }


def generate_topic_chart_data(topics):

    labels = [str(topic[0]) for topic in topics]

    values = [int(topic[1]) for topic in topics]

    return {
        'labels': labels,
        'values': values
    }


def generate_wordcloud(feedback_list):

    text = ' '.join(feedback_list)

    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='black',
        colormap='Blues'
    ).generate(text)

    plt.figure(figsize=(12, 6))

    plt.imshow(wordcloud, interpolation='bilinear')

    plt.axis('off')

    output_path = 'static/images/wordcloud.png'

    plt.savefig(
        output_path,
        bbox_inches='tight',
        facecolor='black'
    )

    plt.close()

    return output_path