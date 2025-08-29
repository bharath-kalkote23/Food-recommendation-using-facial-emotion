import json, math
from typing import List, Dict, Any

# Simple rule+content recommender
EMOTION_TAGS = {
    "happy": ["celebration","sweet","festive","popular"],
    "sad": ["comfort","soothing","mood-lift","light"],
    "angry": ["cooling","fresh","light","soothing"],
    "fearful": ["light","soothing","mild"],
    "surprised": ["new","spicy","aromatic"],
    "neutral": ["popular","healthy","light"]
}

def cosine(a, b):
    # a,b dict tag->weight
    ks = set(a) | set(b)
    num = sum(a.get(k,0)*b.get(k,0) for k in ks)
    da = math.sqrt(sum(v*v for v in a.values()))
    db = math.sqrt(sum(v*v for v in b.values()))
    return 0.0 if da==0 or db==0 else num/(da*db)

def vectorize_tags(tags: List[str]):
    v = {}
    for t in tags:
        v[t] = v.get(t,0)+1.0
    return v

def score_item(item, emotion="neutral", diet=None):
    tags = item.get("tags",[])
    v_item = vectorize_tags(tags)
    v_pref = vectorize_tags(EMOTION_TAGS.get(emotion, EMOTION_TAGS["neutral"]))
    sim = cosine(v_item, v_pref)
    bonus = 0.0
    if diet and diet in (item.get("diet") or []): bonus += 0.15
    if item.get("rating",0) > 4.5: bonus += 0.1
    return sim + bonus

def recommend(menu: List[Dict[str,Any]], emotion="neutral", diet=None, top_k=6):
    ranked = sorted(menu, key=lambda x: score_item(x, emotion, diet), reverse=True)
    if diet:
        # keep diversity but ensure some diet-safe
        diet_items = [m for m in ranked if diet in (m.get("diet") or [])]
        non = [m for m in ranked if m not in diet_items]
        ranked = (diet_items[:max(2, top_k//2)] + non)[:top_k]
    return ranked[:top_k]