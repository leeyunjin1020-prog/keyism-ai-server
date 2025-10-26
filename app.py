from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # 프레이머에서 오는 요청 허용

clf = pipeline("sentiment-analysis")

def pick_key(user_text: str) -> str:
    result = clf(user_text)[0]
    label = result['label'].upper()
    t = user_text.lower()

    if any(w in t for w in ["angry", "화나", "짜증", "빡쳐", "폭발"]):
        return "ANGER"
    if any(w in t for w in ["말 못", "말하기 싫", "조용", "침묵", "지쳤", "불안"]):
        return "SILENCE"
    if any(w in t for w in ["벗어나", "escape", "도망", "자유", "떠나"]):
        return "FREEDOM"
    if any(w in t for w in ["좋아", "사랑", "보고 싶", "그리워", "안아"]):
        return "LOVE"

    if label == "NEGATIVE":
        return "SILENCE"
    if label == "POSITIVE":
        return "LOVE"
    return "FREEDOM"

@app.route("/unlock", methods=["POST"])
def unlock():
    data = request.get_json()
    feeling = data.get("feeling", "")
    key_type = pick_key(feeling)
    return jsonify({"keyType": key_type})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

