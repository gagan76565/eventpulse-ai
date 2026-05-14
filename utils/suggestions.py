def generate_suggestions(complaints):

    suggestions = []

    complaint_text = " ".join(complaints).lower()

    if "registration" in complaint_text:

        suggestions.append(
            "Introduce QR-based fast-track registration."
        )

    if "audio" in complaint_text or "sound" in complaint_text:

        suggestions.append(
            "Perform complete audio testing before sessions."
        )

    if "food" in complaint_text:

        suggestions.append(
            "Improve catering quality and increase serving counters."
        )

    if "seat" in complaint_text or "crowd" in complaint_text:

        suggestions.append(
            "Improve seating management and venue capacity planning."
        )

    if "late" in complaint_text or "delay" in complaint_text:

        suggestions.append(
            "Improve scheduling coordination to reduce delays."
        )

    if len(suggestions) == 0:

        suggestions.append(
            "Continue maintaining overall event quality and attendee engagement."
        )

    return suggestions[:5]