import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI  # 👈 추가

app = Flask(__name__)
CORS(app)

# ✅ OpenAI 클라이언트 생성
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def pick_key(user_text: str) -> str:
    """(선택) 키워드 기반 백업용: 혹시 AI 호출 실패 시 대비"""
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
    return "SILENCE"


# ✅ Render 깨우기용 헬스 체크 라우트
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ✅ 메인: AI 감정 분석 라우트
@app.route("/unlock", methods=["POST"])
def unlock():
    data = request.get_json()
    feeling = data.get("feeling", "")

    try:
        # OpenAI에 감정 분류 요청
        prompt = f"다음 문장의 감정을 ANGER, SILENCE, FREEDOM, LOVE 중 하나로 분류해줘:\n\n'{feeling}'"
        response = client.responses.create(
            model="gpt-4.1-mini",  # gpt-4.1-mini는 빠르고 저렴
            input=prompt,
        )
        key_type = response.output[0].content[0].text.strip().upper()

    except Exception as e:
        print(f"OpenAI API error: {e}")
        # API 실패 시 키워드 기반 fallback
        key_type = pick_key(feeling)

    return jsonify({"keyType": key_type})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
