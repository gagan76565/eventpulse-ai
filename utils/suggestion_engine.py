def generate_suggestions(topics, complaints):

    suggestions = []

    topic_words = [topic[0] for topic in topics]

    topic_text = ' '.join(topic_words)

    if 'audio' in topic_text or 'microphone' in topic_text:

        suggestions.append(
            'Improve audio systems and conduct microphone testing before future sessions.'
        )

    if 'food' in topic_text:

        suggestions.append(
            'Enhance catering quality and increase food variety for attendees.'
        )

    if 'venue' in topic_text or 'crowded' in topic_text:

        suggestions.append(
            'Consider a larger venue or improve seating and crowd management.'
        )

    if 'registration' in topic_text:

        suggestions.append(
            'Optimize the registration and check-in workflow to reduce delays.'
        )

    if 'networking' in topic_text:

        suggestions.append(
            'Expand networking opportunities with structured interaction sessions.'
        )

    if 'workshop' in topic_text or 'handson' in topic_text:

        suggestions.append(
            'Include more hands-on workshops and interactive learning activities.'
        )

    if len(complaints) >= 3:

        suggestions.append(
            'Prioritize recurring attendee complaints during next event planning.'
        )

    if len(suggestions) == 0:

        suggestions.append(
            'Overall feedback sentiment is highly positive. Maintain current event quality standards.'
        )

    return suggestions[:5]