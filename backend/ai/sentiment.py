from textblob import TextBlob

def get_sentiment(text):
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity

    words = text.lower().split()

    negative_words = ["bad", "worst", "poor", "terrible"]
    positive_words = ["good", "nice", "excellent"]

    pos_count = 0
    neg_count = 0

    skip_next = False

    for i in range(len(words)):

        if skip_next:
            skip_next = False
            continue

        word = words[i]

        
        if word == "not" and i + 1 < len(words):
            next_word = words[i + 1]

            if next_word in positive_words:
                neg_count += 2
            elif next_word in negative_words:
                pos_count += 2

            skip_next = True
            continue

        
        if word in positive_words:
            pos_count += 1
        elif word in negative_words:
            neg_count += 2

    
    if neg_count > pos_count:
        return "negative"
    elif pos_count > neg_count:
        return "positive"
    else:
        if score > 0.1:
            return "positive"
        elif score < -0.1:
            return "negative"
        else:
            return "neutral"