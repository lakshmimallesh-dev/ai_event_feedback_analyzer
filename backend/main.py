from fastapi import FastAPI
from database import engine
from models import Base
from database import SessionLocal
from models import Feedback
from ai.sentiment import get_sentiment
from ai.keywords import extract_keywords
from ai.suggestions import generate_suggestions
from fastapi.middleware.cors import CORSMiddleware
from ai.suggestions import generate_summary
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Server running successfully"}
@app.post("/submit")
def submit_feedback(data: dict, db: Session = Depends(get_db)):

    sentiment = get_sentiment(data["comment"])
    keywords = extract_keywords(data["comment"])

    feedback = Feedback(
        name=data["name"],
        event=data["event"],
        rating=data["rating"],
        comment=data["comment"],
        sentiment=sentiment,
        keywords=keywords
    )

    db.add(feedback)
    db.commit()

    return {
        "message": "Feedback saved",
        "sentiment": sentiment,
        "keywords": keywords
    }
@app.get("/feedback")
def get_feedback(db: Session = Depends(get_db)):
    data = db.query(Feedback).all()

    result = []
    for item in data:
        result.append({
            "id": item.id,
            "name": item.name,
            "event": item.event,
            "rating": item.rating,
            "comment": item.comment,
            "sentiment": item.sentiment,
            "keywords": item.keywords
        })

    return result

@app.get("/suggestions")
def get_suggestions(event: str = None, db: Session = Depends(get_db)):
    if event and event != "all":
        data = db.query(Feedback).filter(Feedback.event == event).all()
    else:
        data = db.query(Feedback).all()

    suggestions = generate_suggestions(data)

    return {"suggestions": suggestions}

@app.post("/analyze")
def analyze_feedback(data: dict):
    sentiment = get_sentiment(data["comment"])
    keywords = extract_keywords(data["comment"])

    return {
        "sentiment": sentiment,
        "keywords": keywords
    }

@app.get("/summary")
def summary(event: str = None, db: Session = Depends(get_db)):
    if event and event != "all":
        data = db.query(Feedback).filter(Feedback.event == event).all()
    else:
        data = db.query(Feedback).all()

    if not data:
        return {"summary": None}

    avg_rating = sum([d.rating for d in data]) / len(data)

    sentiments = [d.sentiment for d in data]

    if sentiments.count("positive") > sentiments.count("negative"):
        sentiment = "positive"
    elif sentiments.count("negative") > sentiments.count("positive"):
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "summary": f"Overall sentiment is {sentiment}. Average rating is {round(avg_rating,1)}."
    }



@app.get("/event-insights")
def get_event_insights(event: str = "all", db: Session = Depends(get_db)):
    if event and event != "all":
        data = db.query(Feedback).filter(Feedback.event == event).all()
    else:
        data = db.query(Feedback).all()

    if not data:
        return {
            "best_event": "N/A",
            "worst_event": "N/A",
            "avg_rating": 0,
            "risk": "No Data"
        }

    event_ratings = {}
    event_counts = {}

    for fb in data:
        event_ratings[fb.event] = event_ratings.get(fb.event, 0) + fb.rating
        event_counts[fb.event] = event_counts.get(fb.event, 0) + 1

    avg_scores = {e: event_ratings[e] / event_counts[e] for e in event_ratings}

    best_event = max(avg_scores, key=avg_scores.get)
    worst_event = min(avg_scores, key=avg_scores.get)

    overall_avg = sum(avg_scores.values()) / len(avg_scores)

    risk = "Low" if overall_avg >= 4 else "Medium" if overall_avg >= 2.5 else "High"

    return {
        "best_event": best_event,
        "worst_event": worst_event,
        "avg_rating": round(overall_avg, 2),
        "risk": risk
    }


@app.get("/predict")
def predict_event_success(event: str = None, db: Session = Depends(get_db)):
    if event and event != "all":
        data = db.query(Feedback).filter(Feedback.event == event).all()
    else:
        data = db.query(Feedback).all()

    if not data:
        return {
            "success_rate": 0,
            "prediction": "No Data",
            "confidence": "Low"
        }

    total = len(data)

    positive = sum(1 for fb in data if fb.sentiment == "positive")
    negative = sum(1 for fb in data if fb.sentiment == "negative")

    avg_rating = sum(fb.rating for fb in data) / total

    # 🧠 BETTER AI LOGIC
    if avg_rating >= 4 and positive >= negative:
        prediction = "Event will be successful 🚀"
        confidence = "High"
    elif avg_rating >= 2.5:
        prediction = "Event has moderate success chances ⚠️"
        confidence = "Medium"
    else:
        prediction = "Event likely to fail ❌"
        confidence = "Low"

    success_rate = int((avg_rating / 5) * 100)

    return {
        "success_rate": success_rate,
        "prediction": prediction,
        "confidence": confidence
    }