from collections import Counter

def generate_suggestions(feedback_list):
    issue_keywords = []

    issue_map = {
        "food": "food",
        "music": "music",
        "management": "management",
        "timing": "timing",
        "speaker": "speaker",

        "laptop": "technical",
        "system": "technical",
        "network": "technical",
        "wifi": "technical",
        "projector": "technical",

        "seminar": "content",
        "teaching": "content",
        "session": "content",
        "presentation": "content",
        "workshop": "content"   # ✅ ADD THIS (VERY IMPORTANT)
    }

    negative_words = ["bad", "worst", "poor", "terrible", "not", "waste", "boring"]

    for fb in feedback_list:

        if fb.sentiment == "negative":

            text = fb.comment.lower()

            # 🔥 ensure it's actually negative text
            if not any(nw in text for nw in negative_words):
                continue

            words = text.split()
            found_issue = False

            for w in words:
                clean = w.strip(".,!")

                if clean in issue_map:
                    issue_keywords.append(issue_map[clean])
                    found_issue = True

            # 🔥 fallback ALWAYS
            if not found_issue:
                issue_keywords.append("general")

    print("DEBUG FINAL KEYWORDS:", issue_keywords)

    freq = Counter(issue_keywords)

    suggestions = []

    for word, count in freq.most_common(5):

        if word == "food":
            suggestions.append(f"Improve food quality ({count} complaints)")
        elif word == "music":
            suggestions.append(f"Enhance music experience ({count} complaints)")
        elif word == "management":
            suggestions.append(f"Improve event management ({count} complaints)")
        elif word == "timing":
            suggestions.append(f"Improve event scheduling ({count} complaints)")
        elif word == "speaker":
            suggestions.append(f"Enhance speaker quality ({count} complaints)")
        elif word == "technical":
            suggestions.append(f"Fix technical issues (WiFi, systems) ({count} complaints)")
        elif word == "content":
            suggestions.append(f"Improve session/workshop content ({count} complaints)")
        elif word == "general":
            suggestions.append(f"Improve overall event experience ({count} complaints)")

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

    if negative > positive:
        mood = "Overall sentiment is negative"
    elif positive > negative:
        mood = "Overall sentiment is positive"
    else:
        mood = "Feedback is mixed"

    if avg_rating >= 4:
        rating_msg = "Users are highly satisfied"
    elif avg_rating >= 2.5:
        rating_msg = "User satisfaction is average"
    else:
        rating_msg = "User satisfaction is low"

    return f"{mood}. Average rating is {round(avg_rating, 2)}. {rating_msg}."