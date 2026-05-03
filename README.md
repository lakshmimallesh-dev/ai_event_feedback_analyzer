# 🚀 AI Event Feedback Analyzer

⚡ Transform event feedback into intelligent insights using AI

---

## 📌 Overview

AI Event Feedback Analyzer is a full-stack web application that collects user feedback for events and analyzes it using AI techniques.

It automatically:
- Detects sentiment (positive / negative)
- Extracts important keywords
- Generates smart suggestions
- Predicts event success

---

## 🧠 Features

### 🤖 AI Feedback Analysis
- Sentiment detection using TextBlob
- Handles cases like:
  - "not good" → negative
  - "not bad" → positive

---

### 💡 Smart Suggestions
- Identifies real issues like:
  - food
  - management
  - timing
- Ignores useless words like:
  - good, very, nice

---

### 📊 Dashboard
- Total feedback count
- Positive / Negative stats
- Pie chart visualization
- Event-wise filtering

---

### 🔮 Event Prediction
- Calculates success rate
- Shows:
  - Success %
  - Prediction result
  - Confidence level

---

### 📁 CSV Export
- Download all feedback data

---

### 🔐 Admin Login
- Secure dashboard access

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript
- Chart.js

### Backend
- Python
- FastAPI

### AI / NLP
- TextBlob
- Rule-based keyword extraction

---

## 📂 Project Structure

```bash
event_feedback_ai/
├── backend/
│   ├── main.py              # FastAPI backend
│   ├── suggestions.py       # AI suggestions logic
│   └── sentiment.py         # Sentiment analysis
│
├── frontend/
│   ├── index.html           # Home page
│   ├── dashboard.html       # Admin dashboard
│   ├── login.html           # Admin login
│   ├── feedback.html        # Feedback form
│   ├── style.css            # UI styling
│   └── script.js            # Frontend logic
│
└── README.md

---

## ⚡ How It Works

1. User submits feedback
2. Backend processes:
   - Sentiment
   - Keywords
3. AI generates:
   - Suggestions
   - Summary
   - Prediction
4. Dashboard displays results

---

## 🧪 Example

Input:
"Music is good but food is bad"

Output:
- Sentiment: Negative
- Suggestion: Improve food quality
- Prediction: Moderate success

---

## 🚀 Setup

### 1. Clone Repo
git clone https://github.com/lakshmimallesh-dev/ai_event_feedback_analyzer.git

cd ai_event_feedback_analyzer

---

### 2. Run Backend

cd backend
pip install fastapi uvicorn textblob
uvicorn main:app --reload


---

### 3. Open Frontend
- Open frontend/index.html in browser

---

## 🎯 Use Cases

- College events
- Hackathons
- Workshops
- Corporate events

---

## 🔮 Future Scope

- Machine learning model
- Real-time analytics
- Cloud deployment
- Advanced NLP models

---

## 👨‍💻 Author

Suvarnam Lakshmi Mallesh  
B.Tech CSE (Data Science)

---

## ⭐ Note

This project demonstrates:
- Full-stack development
- AI integration
- Data analysis
- UI design
