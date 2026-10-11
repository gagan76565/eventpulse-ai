"""Input parsing helpers for free-form and labeled attendee feedback."""

import re

_FEEDBACK_LABEL = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?feedback(?:\*\*)?\s*:\s*(.*?)\s*$",
    flags=re.IGNORECASE,
)


def _remove_wrapping_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()
    return value


def split_feedback(text: str) -> list[str]:
    """Extract feedback values from labeled blocks, otherwise split non-empty lines.

    Labeled attendee blocks containing Attendee ID, Rating, and Feedback fields
    produce one response per Feedback field, not one response per metadata line.
    """
    if not text or not text.strip():
        return []

    lines = text.splitlines()
    labeled_feedback = []
    for line in lines:
        match = _FEEDBACK_LABEL.match(line)
        if match:
            value = _remove_wrapping_quotes(match.group(1))
            if value:
                labeled_feedback.append(value)

    if labeled_feedback:
        return labeled_feedback

    return [line.strip() for line in lines if line.strip()]
