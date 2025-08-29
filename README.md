# Facial Emotion Based Food Recommendation 

A smart restaurant web app that personalizes menu recommendations using **facial emotion recognition**, health/diet preferences, and past behavior. It also includes **table reservations**, a **digital menu**, and a lightweight **chatbot**.

> Frontend runs entirely in the browser and uses `face-api.js` (TensorFlow.js models) for facial emotion detection. Backend is a Flask API with SQLite via SQLAlchemy.

---

## Features
- Emotion-aware food suggestions (happy, sad, angry, fearful, surprised, neutral)
- Health-aware personalization (diet: vegan/veg/jain/keto/diabetic/gluten-free)
- Menu search, tags, ratings, and dynamic reordering
- Table reservation (date/time/party size), admin viewer
- Lightweight rule-based + content-based recommender
- Simple chatbot for FAQs
- SQLite storage for users, orders, and reservations

## Tech Stack
- **Frontend:** HTML, TailwindCSS (CDN), face-api.js (CDN), vanilla JS
- **Backend:** Flask (Python), REST endpoints
- **DB:** SQLite (SQLAlchemy models)
- **Data:** `data/menu.json` (sample items with tags & nutrition)

## Quick Start

1) Python 3.10+ recommended.
2) Create and activate a virtual env
```bash
```
3) Install deps:
```bash
pip install -r requirements.txt
```
4) Run the app:
```bash
python app.py
```
5) Open the site:
```
http://127.0.0.1:5000
```

## Project Structure
```
moodbite/
  app.py
  database.py
  models.py
  recommender.py
  requirements.txt
  data/menu.json
  static/
    js/app.js
    js/face.js
    css/styles.css
  templates/
    base.html
    index.html
    menu.html
    reserve.html
    profile.html
    admin.html
```

## Notes
- For emotion detection, the browser will ask camera permission. If denied, you can manually choose an emotion from the dropdown and still get recommendations.
- All endpoints are in `app.py`. Recommender logic in `recommender.py`.
- This is a teaching/project-ready baseline. Extend with authentication, real payment, cloud DB, etc.
