from flask import Flask, render_template, request, send_file
import os
import pandas as pd
import csv

from utils.preprocess import clean_text
from utils.sentiment import analyze_sentiment
from utils.themes import extract_themes
from utils.insights import extract_insights
from utils.suggestions import generate_suggestions
from utils.visualizer import generate_wordcloud

from utils.database import init_db, save_analysis
from utils.summary import generate_summary
from utils.frequency import complaint_frequency

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("exports", exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        feedback_list = []

        # --------------------------------
        # Text Feedback
        # --------------------------------

        pasted_feedback = request.form.get(
            "feedback_text"
        )

        if pasted_feedback:

            feedback_entries = pasted_feedback.split("\n")

            for entry in feedback_entries:

                entry = entry.strip()

                if entry:
                    feedback_list.append(entry)

        # --------------------------------
        # File Upload
        # --------------------------------

        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename != "":

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                uploaded_file.filename
            )

            uploaded_file.save(filepath)

            # CSV

            if uploaded_file.filename.endswith(".csv"):

                df = pd.read_csv(filepath)

                first_column = df.columns[0]

                csv_feedback = df[first_column] \
                    .dropna() \
                    .astype(str) \
                    .tolist()

                feedback_list.extend(csv_feedback)

            # TXT

            elif uploaded_file.filename.endswith(".txt"):

                with open(
                    filepath,
                    "r",
                    encoding="utf-8"
                ) as file:

                    lines = file.readlines()

                    for line in lines:

                        line = line.strip()

                        if line:
                            feedback_list.append(line)

        # --------------------------------
        # Validation
        # --------------------------------

        if len(feedback_list) == 0:

            return render_template(
                "index.html",
                error="Please provide feedback input."
            )

        # --------------------------------
        # Preprocessing
        # --------------------------------

        cleaned_feedback = []

        for feedback in feedback_list:

            cleaned = clean_text(feedback)

            cleaned_feedback.append(cleaned)

        # --------------------------------
        # Sentiment Analysis
        # --------------------------------

        sentiment_results, sentiment_summary = \
            analyze_sentiment(feedback_list)

        # --------------------------------
        # Themes
        # --------------------------------

        themes = extract_themes(
            cleaned_feedback
        )

        # --------------------------------
        # Insights
        # --------------------------------

        complaints, positives = extract_insights(
            sentiment_results
        )

        # --------------------------------
        # Suggestions
        # --------------------------------

        suggestions = generate_suggestions(
            complaints
        )

        # --------------------------------
        # Summary
        # --------------------------------

        summary = generate_summary({

            "total_feedback":
                len(feedback_list),

            "positive_percent":
                sentiment_summary["positive_percent"],

            "negative_percent":
                sentiment_summary["negative_percent"],

            "complaints":
                complaints,

            "positives":
                positives
        })

        # --------------------------------
        # Complaint Frequency
        # --------------------------------

        complaint_freq = complaint_frequency(
            complaints
        )

        # --------------------------------
        # Event Score
        # --------------------------------

        event_score = (
            sentiment_summary["positive_percent"]
            - sentiment_summary["negative_percent"]
            + 50
        )

        event_score = max(0, min(100, event_score))

        # --------------------------------
        # Word Cloud
        # --------------------------------

        wordcloud_image = generate_wordcloud(
            cleaned_feedback
        )

        # --------------------------------
        # Dashboard Data
        # --------------------------------

        dashboard_data = {

            "total_feedback":
                len(feedback_list),

            "positive_percent":
                sentiment_summary["positive_percent"],

            "negative_percent":
                sentiment_summary["negative_percent"],

            "neutral_percent":
                sentiment_summary["neutral_percent"],

            "top_themes":
                themes,

            "complaints":
                complaints,

            "positives":
                positives,

            "suggestions":
                suggestions,

            "summary":
                summary,

            "complaint_frequency":
                complaint_freq,

            "event_score":
                event_score,

            "wordcloud_image":
                wordcloud_image
        }

        save_analysis(dashboard_data)

        return render_template(
            "dashboard.html",
            data=dashboard_data
        )

    except Exception as e:

        return render_template(
            "error.html",
            error_message=str(e)
        )


@app.route("/export")
def export_report():

    export_path = "exports/event_report.csv"

    rows = [
        ["Metric", "Value"],
        ["Project", "EventPulse AI"]
    ]

    with open(
        export_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerows(rows)

    return send_file(
        export_path,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)