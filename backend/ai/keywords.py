def extract_keywords(text):
    words = text.lower().split()

    important = []
    negative_words = ["bad", "worst", "poor", "terrible"]

    for i, word in enumerate(words):
        clean = word.strip(".,!")

        # keep negative words ALSO
        if clean in negative_words:
            important.append(clean)

            # also capture previous word
            if i > 0:
                important.append(words[i - 1])

        else:
            important.append(clean)

    return ", ".join(set(important))