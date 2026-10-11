---
title: EventPulse AI
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# EventPulse AI

**Turn college-event feedback into understandable evidence and practical next steps.** EventPulse AI is a Streamlit analytics app that accepts pasted feedback or CSV/TXT uploads and produces sentiment signals, recurring terms, complaint examples, positive feedback, recommendations, and a downloadable CSV report.

## Features

- Paste one response per line or upload `.csv` / `.txt` files.
- Detect a feedback column in CSV files (`feedback`, `response`, `comment`, `answer`, or `text`) and fall back to a text column.
- Classify each response with VADER sentiment analysis.
- Extract frequent unigrams/bigrams as themes using scikit-learn CountVectorizer.
- Identify likely complaints with transparent keyword rules.
- Generate up to five practical recommendations from themes and complaint volume.
- View sentiment distribution, theme-frequency chart, and word cloud.
- Inspect response-level sentiment and download a CSV analysis report.
- Runs without paid API keys or large transformer models; suitable for CPU-only demos.

> **Interpretation note:** Topic labels are frequent terms/phrases, complaint detection uses a keyword heuristic, and the event index is a simple sentiment-derived indicator—not a validated satisfaction score. Review the underlying responses before making event decisions.

## Tech stack

- Python 3.11
- Streamlit
- pandas, scikit-learn, VADER Sentiment
- Plotly, WordCloud, Matplotlib
- Docker / Hugging Face Spaces

## Run locally

```bash
git clone https://github.com/gagan76565/eventpulse-ai.git
cd eventpulse-ai
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit (normally `http://localhost:8501`).

## Test data

Use `data/sample_feedback.csv`. It includes positive, neutral, and negative examples across speaker sessions, networking, audio, food, venue, and registration. CSV files should have a header row and one feedback response per row in the selected column.

## Hugging Face Spaces (Docker)

1. Create a **Docker** Space with CPU Basic hardware.
2. Upload/connect this repository's files at the Space root.
3. Ensure the Space repository contains `Dockerfile`, `requirements.txt`, `streamlit_app.py`, and the `utils/` directory at its root.
4. Hugging Face builds the image and launches Streamlit on port `7860`.
5. Open **Logs** if the build fails; check dependency installation and application startup messages.

The Docker image runs `streamlit run streamlit_app.py --server.port=7860 --server.address=0.0.0.0`. Do not use the old Flask/Gunicorn start command for this Streamlit deployment.

## Repository layout

```text
streamlit_app.py       Streamlit UI and analysis orchestration
utils/
  preprocessing.py     Basic text normalization
  sentiment.py         VADER sentiment labels and counts
  topic_extraction.py  Frequent term/phrase extraction
  complaint_detector.py Keyword-based complaint detection
  suggestion_engine.py Recommendation rules
  summary_generator.py Rule-based executive summary
  analytics.py         Legacy Flask chart helpers (not used by Streamlit UI)
requirements.txt       Pinned runtime dependencies
Dockerfile             Hugging Face Spaces Docker entry point
data/sample_feedback.csv  Small example dataset
```

## Privacy and limitations

Feedback is processed in the active app session. The application does not intentionally save submissions to a database. Avoid uploading personal or sensitive information. Sentiment classifiers and keyword rules can miss sarcasm, context, negation, multilingual feedback, and implicit complaints; use the results as decision support, not as ground truth.

## Author

Gagan
