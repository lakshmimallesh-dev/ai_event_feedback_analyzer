from collections import Counter

def generate_suggestions(feedback_list):

    issue_keywords = []

    valid_issues = ["food", "music", "management", "timing", "speaker"]

    for fb in feedback_list:

        # Already filtered negative → no need to check "bad"
        if fb.sentiment == "negative" and fb.keywords:

            words = [w.strip().lower() for w in fb.keywords.split(",")]

            for w in words:
                if w in valid_issues:
                    issue_keywords.append(w)

    freq = Counter(issue_keywords)

    suggestions = []

    for word, count in freq.most_common(5):

        if word == "food":
            suggestions.append(f"Improve food quality ({count} complaints)")
        elif word == "music":
            suggestions.append(f"Improve music experience ({count} complaints)")
        elif word == "management":
            suggestions.append(f"Improve event management ({count} complaints)")
        elif word == "timing":
            suggestions.append(f"Improve event timing ({count} complaints)")
        elif word == "speaker":
            suggestions.append(f"Improve speaker quality ({count} complaints)")

    if not suggestions:
        suggestions.append("No major issues detected 🎉")

    return suggestions

def generate_summary(feedback_list):

    if not feedback_list:
        return "No feedback available yet."

    total = len(feedback_list)
    positive = sum(1 for fb in feedback_list if fb.sentiment == "positive")
    negative = sum(1 for fb in feedback_list if fb.sentiment == "negative")

    avg_rating = sum(fb.rating for fb in feedback_list) / total

    # 🧠 AI-like interpretation
    if negative > positive:
        mood = "Overall sentiment is negative"
    elif positive > negative:
        mood = "Overall sentiment is positive"
    else:
        mood = "Feedback is mixed"

    # Rating insight
    if avg_rating >= 4:
        rating_msg = "Users are highly satisfied"
    elif avg_rating >= 2.5:
        rating_msg = "User satisfaction is average"
    else:
        rating_msg = "User satisfaction is low"

    return f"{mood}. Average rating is {round(avg_rating,2)}. {rating_msg}."