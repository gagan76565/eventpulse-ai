from collections import Counter


def complaint_frequency(complaints):

    words = []

    for complaint in complaints:

        for word in complaint.lower().split():

            if len(word) > 3:
                words.append(word)

    common = Counter(words).most_common(10)

    return common