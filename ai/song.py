import os
import json
import requests
import re
import random
from dotenv import load_dotenv
import google.generativeai as genai

# 환경 변수 로드
load_dotenv()

# Gemini API 설정
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel(model_name="gemini-pro")

# 수노 API 토큰
TOKEN = os.getenv("TOKEN")

# 감정 분석
def analyze_emotion(emotion):
    prompt = (
        f"{emotion} 라는 문장에서 나타나는 감정이 "
        "sadness, anger, calm, excitement, hope, love, anxiety, joy 중에서 "
        "어디에 속하는지 2개의 키워드로 알려줘. 다른말 하지말고 두개의 키워드만 콤마로 구분해서 알려줘"
    )
    response = model.generate_content(prompt)
    return response.text.replace("\n", "").split(", ")

# 감정 기반 가사 프롬프트 생성
def generate_lyrics_prompt(emotion):
    prompt = (
        f"{emotion} 라는 감정을 느끼고 있는 사람이 공감할 수 있을만한 "
        "노래 가사를 위한 프롬프트 10개 만들어줘 다른 말은 하지말고 프롬프트만 10개 줘 "
        "너가 만든 프롬프트를 이용해서 수노를 이용해 노래 가사를 작성할거야. "
        "좀 더 구체적으로 적어줘. 사용자의 감정에 맞는 노래 가사를 알아낼거야. 예시는 필요없어. "
        "다양한 스타일을 표현해줘. 사용자의 감정도 좋지만 사용자가 선호하는 가사 스타일을 "
        "찾는데 초점을 맞춰줘. 그냥 다른 문자 없이 한줄로 적어줘. 앞에 숫자하고 . 만 붙여 그리고 영어로 써줘"
    )
    response = model.generate_content(prompt)

    result = response.text
    lines = re.split(r'\n|\r', result)
    lyrics = [line.split('.', 1)[-1].strip() for line in lines if '.' in line]

    return {
        "lyrics": lyrics
    }

# 가사 생성 API 호출
def generate_lyrics(emotion):
    print("generate")

    prompts = generate_lyrics_prompt(emotion)
    lyrics_ids = []

    url = "https://apibox.erweima.ai/api/v1/lyrics"

    for prompt in prompts["lyrics"]:
        payload = json.dumps({
            "prompt": prompt,
            "callBackUrl": "https://api.example.com/callback"
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + TOKEN
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response_json = response.json()

            task_id = response_json.get("data", {}).get("taskId")
            if task_id:
                lyrics_ids.append(task_id)
                print(response_json)
            else:
                print("taskId 없음:", response_json)

        except Exception as e:
            print("요청 오류:", e)

    return {"lyrics": lyrics_ids}

# 가사 결과 가져오기
def get_lyric(lyrics_id):
    url = f"https://apibox.erweima.ai/api/v1/lyrics/record-info?taskId={lyrics_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()

        value = random.randint(0, 1)
        result = response_json["data"]["response"]["data"][value]["text"]
        return result

    except Exception as e:
        print("가사가 아직 완성되지 않았습니다:", e)
        return None

# 특정 가사 생성 요청에 사용된 프롬프트 가져오기
def generate_lyrics_prompt_by_id(lyrics_id: str):
    url = f"https://apibox.erweima.ai/api/v1/lyrics/record-info?taskId={lyrics_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    try:
        response = requests.get(url, headers=headers)
        response_json = response.json()
        result = json.loads(response_json["data"]["param"])["prompt"]
        return result

    except Exception as e:
        print("가사가 아직 완성되지 않았습니다:", e)
        return None
