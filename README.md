# EventPulse AI

AI-powered event feedback analytics platform built using Flask, NLP, and interactive dashboard visualizations.

## Live Features

- Sentiment analysis
- Topic extraction
- Complaint detection
- AI-generated improvement suggestions
- Word cloud visualization
- CSV/TXT feedback upload
- Interactive analytics dashboard
- Modern responsive UI

---

# Tech Stack

## Backend
- Flask
- Python

## AI/NLP
- VaderSentiment
- Scikit-learn
- TF-IDF / CountVectorizer

## Frontend
- Tailwind CSS
- Chart.js

## Data Processing
- Pandas
- NumPy

## Visualization
- Matplotlib
- WordCloud

---

# Features

## AI Feedback Analysis
Automatically:
- Detects positive/negative sentiment
- Extracts common themes
- Identifies complaints
- Generates actionable insights

## Dashboard Analytics
- Sentiment charts
- Theme frequency visualization
- Word cloud generation
- AI-generated event summary

## Upload Support
- CSV files
- TXT files
- Manual feedback paste

---

# Project Structure

```text
eventpulse-ai/
│
├── app.py
├── requirements.txt
├── Dockerfile
│
├── templates/
├── static/
├── utils/
└── data/
```

---

# Installation

```bash
git clone <your-repo-link>

cd eventpulse-ai

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

---

# Deployment

Deployed using:
- Hugging Face Spaces
- Docker
- Gunicorn

---

# Future Improvements

- Transformer-based summarization
- Multi-event trend comparison
- PDF report export
- Authentication system
- Real-time analytics

---

# Author

Built by Gagan