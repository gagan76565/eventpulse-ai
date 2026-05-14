def generate_summary(data):

    summary = []

    summary.append(
        f"The event received {data['total_feedback']} feedback responses."
    )

    summary.append(
        f"{data['positive_percent']}% of attendees shared positive feedback."
    )

    if data["negative_percent"] > 30:

        summary.append(
            "Several attendees highlighted operational improvement areas."
        )

    else:

        summary.append(
            "Overall attendee satisfaction remained strong."
        )

    if len(data["complaints"]) > 0:

        summary.append(
            f"Common concerns included {data['complaints'][0].lower()}."
        )

    if len(data["positives"]) > 0:

        summary.append(
            f"Attendees especially appreciated {data['positives'][0].lower()}."
        )

    return " ".join(summary)