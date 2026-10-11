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
_CONTRAST_PATTERN = re.compile(
    r"\s+(?:however|although|though|but|yet|on top of that)\s+",
    flags=re.IGNORECASE,
)
# Common issue subjects help separate criticism from praise even when the
# attendee omits punctuation and words such as "but" or "though".
_ISSUE_SUBJECT_PATTERN = re.compile(
    r"\b(?:the event app|the audio|the venue|the lunch lines?|the parking lot|"
    r"the advanced track sessions?|the breakout rooms?|no clear signage)\b",
    flags=re.IGNORECASE,
)


def detect_complaints(feedback_list):
    """Return unique responses/clauses containing explicit complaint signals."""
    complaints = []
    seen = set()

    for feedback in feedback_list or []:
        original = re.sub(r"\s+", " ", str(feedback)).strip()
        if not original:
            continue

        clauses = []
        for piece in _CONTRAST_PATTERN.split(original):
            clauses.extend(re.split(r"(?<=[.!?])\s+", piece))

        candidates = []
        for clause in clauses:
            clause = clause.strip(" .,!;:-")
            if not clause or not _KEYWORD_PATTERN.search(clause):
                continue

            subject = _ISSUE_SUBJECT_PATTERN.search(clause)
            if (
                subject
                and not _KEYWORD_PATTERN.search(clause[:subject.start()])
                and _KEYWORD_PATTERN.search(clause[subject.start():])
            ):
                clause = clause[subject.start():].strip(" .,!;:-")
            candidates.append(clause)

        if not candidates and _KEYWORD_PATTERN.search(original):
            candidates = [original]

        for candidate in candidates:
            key = candidate.casefold()
            if key not in seen:
                complaints.append(candidate)
                seen.add(key)

    return complaints
