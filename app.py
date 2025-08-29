from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import json, os
from datetime import datetime

from models import User, Reservation
from database import init_db, SessionLocal
from recommender import recommend

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

MENU_PATH = os.path.join('data','menu.json')

@app.before_request
def setup():
    if not hasattr(app, "_db_initialized"):
        init_db()
        app._db_initialized = True


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

@app.route('/reserve')
def reserve_page():
    return render_template('reserve.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

# ---- API ----
@app.route('/api/menu')
def api_menu():
    items = json.load(open(MENU_PATH,'r',encoding='utf-8'))
    return jsonify({"items": items})

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    body = request.get_json(force=True) or {}
    emotion = (body.get('emotion') or 'neutral').lower()
    diet = (body.get('diet') or '').lower() or None
    top_k = int(body.get('top_k') or 6)
    menu = json.load(open(MENU_PATH,'r',encoding='utf-8'))
    items = recommend(menu, emotion=emotion, diet=diet, top_k=top_k)
    return jsonify({"items": items, "emotion": emotion, "diet": diet})

@app.route('/api/reserve', methods=['POST'])
def api_reserve():
    body = request.get_json(force=True) or {}
    with SessionLocal() as db:
        r = Reservation(
            name=body.get('name','Guest'),
            phone=body.get('phone',''),
            date=body.get('date',''),
            time=body.get('time',''),
            size=int(body.get('size') or 2)
        )
        db.add(r)
        db.commit()
    return jsonify({"message":"Reservation confirmed!"})

@app.route('/api/reservations')
def api_reservations():
    with SessionLocal() as db:
        rows = db.query(Reservation).order_by(Reservation.id.desc()).all()
        items = [{
            "name":x.name, "phone":x.phone, "date":x.date, "time":x.time, "size":x.size
        } for x in rows]
    return jsonify({"items": items})

@app.route('/api/profile', methods=['POST'])
def api_profile():
    body = request.get_json(force=True) or {}
    name = body.get('name','Guest')
    diet = body.get('diet','')
    with SessionLocal() as db:
        u = db.query(User).first()
        if not u:
            u = User(name=name, diet=diet)
            db.add(u)
        else:
            u.name = name or u.name
            u.diet = diet or u.diet
        db.commit()
    return jsonify({"message":"Profile saved."})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    q = (request.get_json(force=True) or {}).get('q','').lower()
    if any(k in q for k in ["hour","time","open","close"]):
        a = "We are open daily 11:00–23:00. Last order at 22:30."
    elif any(k in q for k in ["diet","vegan","veg","jain","keto","gluten","diabetic"]):
        a = "We support Veg, Jain, Keto, Gluten-free, and Diabetic-friendly options. Try the filters or set your profile diet."
    elif "reserve" in q or "table" in q or "booking" in q:
        a = "Use the Reserve page to book a table. You’ll get instant confirmation here."
    elif "price" in q or "cost" in q:
        a = "Most mains are ₹120–₹280. Desserts and soups are around ₹90–₹180."
    else:
        a = "I can help with hours, reservations, diets, or menu suggestions. Ask me anything!"
    return jsonify({"a": a})

if __name__ == '__main__':
    app.run(debug=True)