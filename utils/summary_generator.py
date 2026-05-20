def generate_summary(
    positive_count,
    negative_count,
    neutral_count,
    topics
):

    top_topics = ', '.join([
        topic[0]
        for topic in topics[:3]
    ])

    if positive_count > negative_count:

        overall = 'Overall attendee sentiment was largely positive.'

    elif negative_count > positive_count:

        overall = 'Attendee feedback highlighted several improvement areas.'

    else:

        overall = 'Attendee sentiment was balanced between positive and negative experiences.'

    summary = f"""
    {overall}

    The most discussed event themes were:
    {top_topics}.

    Positive responses: {positive_count}
    Negative responses: {negative_count}
    Neutral responses: {neutral_count}
    """

    return summary