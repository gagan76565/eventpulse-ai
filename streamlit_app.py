from __future__ import annotations

import io
import re
from typing import Iterable

import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud

from utils.preprocessing import clean_text
from utils.input_parser import split_feedback
from utils.sentiment import analyze_sentiment
from utils.topic_extraction import extract_topics
from utils.complaint_detector import detect_complaints
from utils.suggestion_engine import generate_suggestions
from utils.summary_generator import generate_summary


st.set_page_config(
    page_title="EventPulse AI | Feedback Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp { background: radial-gradient(circle at 10% 0%, #172554 0, #0b1120 42%, #070b14 100%); }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1440px; padding-top: 2rem; padding-bottom: 3rem; }
    .hero { padding: 1.6rem 1.8rem; border: 1px solid rgba(148,163,184,.22); border-radius: 22px;
            background: linear-gradient(120deg, rgba(30,64,175,.24), rgba(15,23,42,.72)); margin-bottom: 1.25rem; }
    .eyebrow { text-transform: uppercase; letter-spacing: .16em; color: #93c5fd; font-size: .76rem; font-weight: 700; }
    .hero h1 { margin: .35rem 0 .5rem; font-size: clamp(2rem, 4vw, 3.25rem); color: #f8fafc; }
    .hero p { color: #cbd5e1; max-width: 850px; font-size: 1.05rem; margin-bottom: 0; }
    .section-title { margin-top: .6rem; color: #e2e8f0; font-weight: 700; }
    div[data-testid="stMetric"] { background: rgba(15,23,42,.75); border: 1px solid rgba(148,163,184,.2);
      border-radius: 16px; padding: 1rem 1.1rem; }
    .insight-card { border: 1px solid rgba(148,163,184,.2); border-radius: 16px; padding: 1rem;
      background: rgba(15,23,42,.58); margin-bottom: .6rem; }
    .muted { color: #94a3b8; font-size: .9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def read_uploaded_feedback(uploaded_file) -> list[str]:
    if uploaded_file is None:
        return []

    name = uploaded_file.name.lower()
    try:
        if name.endswith(".csv"):
            frame = pd.read_csv(uploaded_file)
            if frame.empty or len(frame.columns) == 0:
                return []
            preferred = next(
                (c for c in frame.columns if str(c).strip().lower() in
                 {"feedback", "response", "comment", "comments", "answer", "text"}),
                None,
            )
            if preferred is None:
                text_columns = [
                    c for c in frame.columns
                    if pd.api.types.is_object_dtype(frame[c]) or
                    pd.api.types.is_string_dtype(frame[c])
                ]
                preferred = text_columns[0] if text_columns else frame.columns[0]
            return [
                str(value).strip()
                for value in frame[preferred].dropna().tolist()
                if str(value).strip() and str(value).strip().lower() != "nan"
            ]

        if name.endswith(".txt"):
            content = uploaded_file.getvalue().decode("utf-8-sig", errors="replace")
            return split_feedback(content)
    except Exception as exc:
        raise ValueError(f"Could not read {uploaded_file.name}: {exc}") from exc

    raise ValueError("Upload a CSV or TXT file.")


def build_wordcloud(feedback: Iterable[str]):
    text = " ".join(feedback).strip()
    if not text or not re.search(r"[A-Za-z]", text):
        return None
    cloud = WordCloud(
        width=1200,
        height=600,
        background_color="#0b1120",
        colormap="winter",
        max_words=100,
        collocations=False,
        min_font_size=8,
    ).generate(text)
    return cloud.to_image()


def analyze(feedback: list[str]) -> dict:
    cleaned = [clean_text(item) for item in feedback]
    # Keep original wording for sentiment and complaint detection: removing
    # words such as "not" during preprocessing can reverse the meaning.
    sentiment = analyze_sentiment(feedback)
    topics = extract_topics([text for text in cleaned if text.strip()], top_n=10)
    complaints = detect_complaints(feedback)
    suggestions = generate_suggestions(topics, complaints)
    summary = generate_summary(
        sentiment["positive"],
        sentiment["negative"],
        sentiment["neutral"],
        topics,
    )
    total = len(feedback)
    positive_pct = round(sentiment["positive"] * 100 / total)
    negative_pct = round(sentiment["negative"] * 100 / total)
    neutral_pct = round(sentiment["neutral"] * 100 / total)
    # Transparent heuristic index, not a validated satisfaction measurement.
    event_score = round(
        100 * (sentiment["positive"] + 0.5 * sentiment["neutral"]) / total
    )
    return {
        "feedback": feedback,
        "sentiment_results": sentiment["results"],
        "positive": sentiment["positive"],
        "negative": sentiment["negative"],
        "neutral": sentiment["neutral"],
        "positive_pct": positive_pct,
        "negative_pct": negative_pct,
        "neutral_pct": neutral_pct,
        "topics": topics,
        "complaints": complaints[:10],
        "positives": [
            item["text"] for item in sentiment["results"]
            if item["sentiment"] == "Positive"
        ][:10],
        "suggestions": suggestions[:5],
        "summary": summary.strip(),
        "event_score": event_score,
        "wordcloud": build_wordcloud(feedback),
    }


def report_csv(result: dict) -> bytes:
    rows = []
    rows.append({"Section": "Overview", "Item": "Total feedback", "Value": len(result["feedback"])})
    rows.append({"Section": "Overview", "Item": "Positive responses", "Value": result["positive"]})
    rows.append({"Section": "Overview", "Item": "Negative responses", "Value": result["negative"]})
    rows.append({"Section": "Overview", "Item": "Neutral responses", "Value": result["neutral"]})
    rows.append({"Section": "Overview", "Item": "Event score (heuristic / 100)", "Value": result["event_score"]})
    rows.append({"Section": "Summary", "Item": "Event summary", "Value": result["summary"]})
    for topic, count in result["topics"]:
        rows.append({"Section": "Theme", "Item": topic, "Value": int(count)})
    for index, complaint in enumerate(result["complaints"], start=1):
        rows.append({"Section": "Complaint", "Item": f"Complaint {index}", "Value": complaint})
    for index, suggestion in enumerate(result["suggestions"], start=1):
        rows.append({"Section": "Recommendation", "Item": f"Suggestion {index}", "Value": suggestion})
    output = io.StringIO()
    pd.DataFrame(rows).to_csv(output, index=False)
    return output.getvalue().encode("utf-8-sig")


st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Event intelligence · NLP analytics</div>
      <h1>EventPulse AI</h1>
      <p>Turn attendee feedback into clear themes, sentiment signals, recurring complaints,
      and practical actions for your next event.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Feedback workspace")
    st.caption("Paste responses or upload a CSV/TXT file. Labeled attendee blocks are parsed from their Feedback fields; plain text uses one response per line.")
    st.markdown("---")
    st.markdown("**Analysis pipeline**")
    st.write("1. Text normalization")
    st.write("2. VADER sentiment scoring")
    st.write("3. TF-IDF-style term counting")
    st.write("4. Complaint and recommendation rules")
    st.markdown("---")
    st.caption("Feedback is analyzed in the current session and is not intentionally stored in a database.")

left, right = st.columns([1.25, 0.75], gap="large")
with left:
    pasted_text = st.text_area(
        "Paste feedback responses",
        height=230,
        placeholder="The speakers were excellent\nRegistration took too long\nLoved the hands-on workshop",
        help="Use one response per line, or paste structured attendee blocks with Attendee ID, Rating, and Feedback labels. Structured blocks are counted by Feedback fields only.",
    )
with right:
    uploaded_file = st.file_uploader(
        "Upload feedback file",
        type=["csv", "txt"],
        help="CSV should contain a feedback/response/comment/text column, or a text column as its first column.",
    )
    st.info("Tip: Use the sample CSV in the repository's data/ folder to try the app.")

if pasted_text.strip() and uploaded_file is not None:
    st.warning("Both pasted feedback and the uploaded file will be analyzed. If they contain the same responses, they will be counted twice.")

run_analysis = st.button("Analyze feedback", type="primary", use_container_width=True)

if run_analysis:
    try:
        feedback = split_feedback(pasted_text or "")
        feedback.extend(read_uploaded_feedback(uploaded_file))
        feedback = [item for item in feedback if item.strip()]
        if not feedback:
            st.session_state.pop("eventpulse_result", None)
            st.error("Add feedback in the text box or upload a CSV/TXT file before analyzing.")
        elif len(feedback) > 5000:
            st.error("Please analyze at most 5,000 responses per run to keep the demo responsive.")
        else:
            # Avoid exact duplicate rows distorting the counts while preserving
            # distinct responses that happen to express the same opinion.
            with st.spinner(f"Analyzing {len(feedback)} feedback responses…"):
                result = analyze(feedback)
                st.session_state["eventpulse_result"] = result
    except (ValueError, UnicodeDecodeError, pd.errors.ParserError) as exc:
        st.error(str(exc))
    except Exception:
        # Keep implementation details out of the public app; diagnose via Space logs.
        st.error("Analysis could not be completed. Check the uploaded file format and try again. If the problem persists, inspect the Space logs.")

result = st.session_state.get("eventpulse_result")

if result:
    st.markdown("## Event overview")
    st.caption(f"Analyzed {len(result['feedback'])} responses in this session.")
    metrics = st.columns(5)
    metrics[0].metric("Responses", len(result["feedback"]))
    metrics[1].metric("Positive", f"{result['positive_pct']}%", f"{result['positive']} responses")
    metrics[2].metric("Negative", f"{result['negative_pct']}%", f"{result['negative']} responses")
    metrics[3].metric("Neutral", f"{result['neutral_pct']}%", f"{result['neutral']} responses")
    metrics[4].metric("Event index", f"{result['event_score']}/100")
    st.caption("Event index is a simple sentiment-derived heuristic for comparing feedback batches, not a validated satisfaction score.")

    st.markdown("## Executive summary")
    st.info(result["summary"])

    chart_col, cloud_col = st.columns(2, gap="large")
    with chart_col:
        st.markdown("### Sentiment distribution")
        sentiment_frame = pd.DataFrame({
            "Sentiment": ["Positive", "Negative", "Neutral"],
            "Responses": [result["positive"], result["negative"], result["neutral"]],
        })
        fig = px.pie(
            sentiment_frame,
            names="Sentiment",
            values="Responses",
            hole=0.58,
            color="Sentiment",
            color_discrete_map={"Positive": "#22c55e", "Negative": "#f87171", "Neutral": "#fbbf24"},
        )
        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title_text="",
        )
        st.plotly_chart(fig, use_container_width=True)
    with cloud_col:
        st.markdown("### Feedback word cloud")
        if result["wordcloud"] is not None:
            st.image(result["wordcloud"], use_container_width=True)
        else:
            st.caption("Not enough readable text to generate a word cloud.")

    st.markdown("## What attendees talked about")
    topic_col, complaint_col = st.columns(2, gap="large")
    with topic_col:
        st.markdown("### Recurring themes")
        if result["topics"]:
            topic_frame = pd.DataFrame(result["topics"], columns=["Theme", "Mentions"])
            topic_frame["Mentions"] = topic_frame["Mentions"].astype(int)
            topic_fig = px.bar(
                topic_frame.sort_values("Mentions"),
                x="Mentions",
                y="Theme",
                orientation="h",
                color="Mentions",
                color_continuous_scale="Blues",
            )
            topic_fig.update_layout(
                template="plotly_dark",
                margin=dict(l=5, r=5, t=10, b=5),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                xaxis_title="Term frequency",
                yaxis_title="",
            )
            st.plotly_chart(topic_fig, use_container_width=True)
            st.caption("Themes are frequent terms/phrases, not guaranteed semantic clusters.")
        else:
            st.write("No recurring themes could be extracted from this input.")
    with complaint_col:
        st.markdown("### Common complaints")
        if result["complaints"]:
            for complaint in result["complaints"]:
                with st.container(border=True):
                    st.warning(complaint)
        else:
            st.success("No complaint matched the current complaint-detection rules.")
            st.caption("This does not guarantee that the feedback contains no problems.")

    st.markdown("## Positive feedback signals")
    positives = result["positives"]
    if positives:
        for positive in positives[:5]:
            with st.container(border=True):
                st.success(positive)
    else:
        st.caption("No responses were classified as positive by the sentiment model.")

    st.markdown("## Recommended actions for the next event")
    if result["suggestions"]:
        for i, suggestion in enumerate(result["suggestions"], start=1):
            with st.container(border=True):
                st.markdown(f"**{i}.** {suggestion}")
    else:
        st.caption("No recommendations were generated for this batch.")

    with st.expander("Inspect every response and its sentiment"):
        detail_frame = pd.DataFrame(result["sentiment_results"])
        detail_frame.columns = ["Feedback response", "Sentiment", "VADER compound score"]
        st.dataframe(detail_frame, use_container_width=True, hide_index=True)

    st.download_button(
        "Download analysis report (CSV)",
        data=report_csv(result),
        file_name="eventpulse_analysis_report.csv",
        mime="text/csv",
        type="primary",
    )
else:
    st.markdown("## What you will get")
    preview_cols = st.columns(3)
    preview_cols[0].markdown("**Sentiment signals**\n\nPositive, negative, and neutral response counts.")
    preview_cols[1].markdown("**Recurring issues**\n\nFrequently mentioned terms and complaint examples.")
    preview_cols[2].markdown("**Actionable next steps**\n\nRecommendations based on detected event pain points.")
