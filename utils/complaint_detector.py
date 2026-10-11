"""Rule-based extraction of complaint-focused clauses from attendee feedback."""

import re

# Explicitly negative event-experience signals. These are transparent heuristics,
# not a substitute for reviewing feedback in context.
NEGATIVE_KEYWORDS = (
    "bad", "poor", "low", "crowded", "overcrowded", "slow", "terrible",
    "boring", "confusing", "noise", "noisy", "issue", "issues", "problem",
    "problems", "disaster", "delay", "delayed", "late", "insufficient",
    "uncomfortable", "frustrating", "failed", "failure", "difficult",
    "disappointing", "disappointed", "improve", "improvement", "lack",
    "missing", "long queue", "long lines", "too long", "freezing",
    "crashing", "crashed", "cutting out", "too basic", "sales pitch",
    "not clear", "no clear signage", "full", "missed", "not enough",
    "could be better", "needs improvement", "kept crashing",
)

_KEYWORD_PATTERN = re.compile(
    r"(?<!\w)(?:" + "|".join(re.escape(word) for word in sorted(NEGATIVE_KEYWORDS, key=len, reverse=True)) + r")(?!\w)",
    flags=re.IGNORECASE,
)
# Reviews often combine praise and criticism in one response without punctuation.
_CONTRAST_PATTERN = re.compile(
    r"\s+(?:however|although|though|but|yet|on top of that)\s+",
    flags=re.IGNORECASE,
)


def detect_complaints(feedback_list):
    """Return only responses/clauses with explicit complaint signals.

    Contrast markers separate praise from criticism when possible, so a mixed
    review does not get shown as a complaint in its entirety.
    """
    complaints = []
    seen = set()

    for feedback in feedback_list or []:
        original = re.sub(r"\s+", " ", str(feedback)).strip()
        if not original:
            continue

        # Split at contrast markers and sentence boundaries, then keep only
        # clauses with an explicit negative signal.
        clauses = [
            clause.strip(" .,!;:-")
            for piece in _CONTRAST_PATTERN.split(original)
            for clause in re.split(r"(?<=[.!?])\s+", piece)
            if clause.strip(" .,!;:-")
        ]
        matched = [clause for clause in clauses if _KEYWORD_PATTERN.search(clause)]

        # Preserve the original response if it is clearly complaint-focused
        # but punctuation/wording prevents a useful clause-level extraction.
        candidates = matched or ([original] if _KEYWORD_PATTERN.search(original) else [])
        for candidate in candidates:
            key = candidate.casefold()
            if key not in seen:
                complaints.append(candidate)
                seen.add(key)

    return complaints
