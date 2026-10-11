import re

# Transparent, deliberately lightweight rules. These are candidate complaints,
# not a substitute for reviewing the original response and its context.
NEGATIVE_KEYWORDS = (
    "bad", "poor", "low", "crowded", "overcrowded", "slow", "terrible",
    "boring", "confusing", "noise", "noisy", "issue", "issues", "problem",
    "problems", "delay", "delayed", "late", "insufficient", "uncomfortable",
    "frustrating", "failed", "failure", "difficult", "disappointing",
    "improve", "improvement", "lack", "missing", "long queue", "too hot",
    "not enough", "could be better", "needs improvement",
)


def detect_complaints(feedback_list):
    complaints = []
    seen = set()

    for feedback in feedback_list or []:
        original = str(feedback).strip()
        if not original:
            continue
        text = re.sub(r"\s+", " ", original.lower())
        if any(
            re.search(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", text)
            for keyword in NEGATIVE_KEYWORDS
        ):
            # Preserve original order while avoiding duplicate complaint cards.
            key = text.casefold()
            if key not in seen:
                complaints.append(original)
                seen.add(key)

    return complaints
