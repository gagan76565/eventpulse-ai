from flask import Flask, render_template, request
import pandas as pd

from utils.preprocessing import clean_text
from utils.sentiment import analyze_sentiment
from utils.topic_extraction import extract_topics
from utils.complaint_detector import detect_complaints
from utils.suggestion_engine import generate_suggestions
from utils.summary_generator import generate_summary

from utils.analytics import (
    generate_sentiment_chart_data,
    generate_topic_chart_data,
    generate_wordcloud
)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    feedback_list = []

    feedback_text = request.form.get('feedback')

    if feedback_text:

        feedback_list.extend([
            line.strip()
            for line in feedback_text.split('\n')
            if line.strip()
        ])

    uploaded_file = request.files.get('file')

    if uploaded_file and uploaded_file.filename != '':

        if uploaded_file.filename.endswith('.csv'):

            df = pd.read_csv(uploaded_file)

            first_column = df.columns[0]

            feedback_list.extend(
                df[first_column]
                .dropna()
                .astype(str)
                .tolist()
            )

        elif uploaded_file.filename.endswith('.txt'):

            content = uploaded_file.read().decode('utf-8')

            feedback_list.extend([
                line.strip()
                for line in content.split('\n')
                if line.strip()
            ])

    if len(feedback_list) == 0:

        return render_template(
            'index.html',
            error='Please provide feedback text or upload a file.'
        )

    cleaned_feedback = [
        clean_text(text)
        for text in feedback_list
    ]

    sentiment_data = analyze_sentiment(cleaned_feedback)

    topics = extract_topics(cleaned_feedback)

    complaints = detect_complaints(cleaned_feedback)

    suggestions = generate_suggestions(topics, complaints)

    summary = generate_summary(
        sentiment_data['positive'],
        sentiment_data['negative'],
        sentiment_data['neutral'],
        topics
    )

    sentiment_chart = generate_sentiment_chart_data(
        sentiment_data['positive'],
        sentiment_data['negative'],
        sentiment_data['neutral']
    )

    topic_chart = generate_topic_chart_data(topics)

    wordcloud_image = generate_wordcloud(cleaned_feedback)

    return render_template(
        'dashboard.html',
        feedbacks=sentiment_data['results'],
        total_feedback=len(cleaned_feedback),
        positive_count=sentiment_data['positive'],
        negative_count=sentiment_data['negative'],
        neutral_count=sentiment_data['neutral'],
        topics=topics,
        complaints=complaints,
        suggestions=suggestions,
        sentiment_chart=sentiment_chart,
        topic_chart=topic_chart,
        summary=summary,
        wordcloud_image=wordcloud_image
    )


if __name__ == '__main__':
    app.run(debug=True)