from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def pick_key(user_text: str) -> str:
    t = user_text.lower()

    anger_keywords = [
        "angry", "화나", "화나서", "짜증", "짜증나", "빡쳐", "열받", "분노", "폭발할 것 같"
    ]
    silence_keywords = [
        "말 못", "말하기 싫", "조용", "침묵", "지쳤", "불안", "무서워",
        "숨막혀", "답답", "힘들어", "피곤해", "울고 싶"
    ]
    freedom_keywords = [
        "벗어나", "escape", "도망", "도망치고 싶", "자유", "떠나", "해방",
        "여기서 나가고 싶", "풀려나고 싶"
    ]
    love_keywords = [
        "좋아", "사랑", "보고 싶", "그리워", "따뜻", "안아", "안아줬으면",
        "연결되고 싶", "기대고 싶"
    ]

    if any(w in t for w in anger_keywords):
        return "ANGER"
    if any(w in t for w in silence_keywords):
        return "SILENCE"
    if any(w in t for w in freedom_keywords):
        return "FREEDOM"
    if any(w in t for w in love_keywords):
        return "LOVE"

    # 키워드가 하나도 안 걸리면 기본적으로 'SILENCE'로 보냄
    return "SILENCE"

@app.route("/unlock", methods=["POST"])
def unlock():
    data = request.get_json()
    feeling = data.get("feeling", "")
    key_type = pick_key(feeling)
    return jsonify({"keyType": key_type})

if __name__ == "__main__":
    # Render 등 PaaS에서 필요: 외부에서 접근 가능한 host로 열기
    app.run(host="0.0.0.0", port=5000)
