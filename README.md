# EventPulse AI 

AI-powered event feedback analysis platform built using Flask, NLP, Machine Learning, and Tailwind CSS.

---

# Live Demo

(Add Render Deployment Link Here)

---

# Features

- Upload CSV/TXT feedback files
- Paste attendee feedback directly
- Sentiment analysis using VADER
- Theme/topic detection using TF-IDF + KMeans
- AI-generated event summaries
- Complaint frequency analysis
- Smart improvement suggestions
- Word cloud visualization
- Interactive analytics dashboard
- SQLite-based analysis storage
- Export analytics reports

---

# Tech Stack

## Backend
- Flask
- Python

## AI/NLP
- Scikit-learn
- TF-IDF
- KMeans Clustering
- VADER Sentiment Analysis
- NLTK

## Frontend
- Tailwind CSS
- Chart.js

## Database
- SQLite

## Deployment
- Render
- Gunicorn

---

# Project Architecture

User Feedback
↓
Text Preprocessing
↓
Sentiment Analysis
↓
Theme Detection
↓
Complaint Extraction
↓
AI Suggestion Engine
↓
Analytics Dashboard

---

# Screenshots

(Add screenshots here later)

---

# Installation

## Clone Repository

```bash
git clone <your-repo-link>
```

## Open Project

```bash
cd eventpulse-ai
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Download NLTK Resources

```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

## Run Application

```bash
python app.py
```

---

# Sample Test Files

Use files inside:

```plaintext
sample_data/
```

---

# Deployment

This project is optimized for Render deployment using:

- Gunicorn
- Lightweight NLP models
- SQLite
- Production-safe dependency versions

---

# Future Improvements

- OpenAI/Gemini integration
- Multi-event comparison
- Admin authentication
- PDF analytics export
- Real-time analytics API

---

# Author

Gagan

---
