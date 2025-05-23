import os
import json
import requests
import random
from dotenv import load_dotenv
import google.generativeai as genai

from data import song as data

from error import IdNotFoundException, InvalidEmotionResultException

# 환경 변수 로드
load_dotenv()

# Gemini API 설정
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# 수노 API 토큰
TOKEN = os.getenv("TOKEN")

# suno - noTOKEN - 가사 결과 가져오기
def get_lyrics(lyrics_id):
    url = f"https://apibox.erweima.ai/api/v1/lyrics/record-info?taskId={lyrics_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    response = requests.get(url, headers=headers)
    print(type(response))
    print(response.text)
    response = json.loads(response.text)

    return response

# gemini - 감정 분석
def analyze_emotion(emotion):
    prompt = (
        f"{emotion} 라는 문장에서 나타나는 감정이 "
        "sadness, anger, calm, excitement, hope, love, anxiety, joy 중에서 "
        "어디에 속하는지 2개의 키워드로 알려줘. 다른말 하지말고 두개의 키워드만 콤마로 구분해서 알려줘 영어로 알려줘 내가 말한 키워드 말고 다른 키워드는 쓰지마"
    )

    result = model.generate_content(prompt)

    print(result)

    return result

# suno - 가사 생성 API 호출
def generate_lyrics(prompt):
    url = "https://apibox.erweima.ai/api/v1/lyrics"

    payload = json.dumps({
        "prompt": prompt,
        "callBackUrl": "https://api.example.com/callback"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    response = requests.post(url, headers=headers, data=payload)
    response = json.loads(response.text)

    print(response)

    return response

# gemini - 감정 기반 가사 프롬프트 생성
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

    return result

# suno - noTOKEN - 특정 가사 생성 요청에 사용된 프롬프트 가져오기
def get_lyrics_prompt_by_id(lyrics_id: str):
    url = f"https://apibox.erweima.ai/api/v1/lyrics/record-info?taskId={lyrics_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    try:
        response = requests.get(url, headers=headers)
        response_json = json.loads(response.text)
        print("response_json", response_json)
        result = json.loads(response_json["data"]["param"])["prompt"]
        print("result", result)
        return result

    except Exception as e:
        print("가사가 아직 완성되지 않았습니다:", e)
        return None

# gemini - 여러개의 가사 프롬프트를 하나로
def generate_one_lyrics(lyrics_prompts):
    prompt = (
        f"{lyrics_prompts} 라는 5개의 예시 프롬프트들을 하나의 프롬프트로 만들어줘. "
        "예시 프롬프트의 모든 내용을 다 반영해줘. "
        "너가 만든 프롬프트를 이용해서 수노를 이용해 노래 가사를 작성할거야. "
        "1000자 이내로 작성해줘. 5개의 샘플 프롬프트를 한 문장으로 압축시켜줘 프롬프트 한 문장만 출력하고 다른 말은 절대 하지마"
    )
    lyrics = model.generate_content(prompt).text
    print("lyrics", lyrics)

    return lyrics

# gemini - 여러개의 멜로디 프롬프트를 하나로
def generate_one_melody(melody_prompts):
    prompt = (
        f"{melody_prompts} 라는 10개의 예시 프롬프트들을 하나의 프롬프트로 만들어줘. "
        "예시 프롬프트의 모든 내용을 다 반영해줘. "
        "너가 만든 프롬프트를 이용해서 수노를 이용해 멜로디를 작성할거야. "
        "1000자 이내로 작성해줘. 10개의 샘플 프롬프트를 한 문장으로 압축시켜줘. 프롬프트 한 문장만 출력하고 다른 말은 절대 하지마"
    )
    melody = model.generate_content(prompt).text
    print("melody", melody)

    return melody

# gemini - 가사, 멜로디 프롬프트로 제목 만들기
def generate_title(lyrics_prompts, melody_prompts):
    prompt = (
        f"가사 프롬프트: {lyrics_prompts} "
        f"멜로디 프롬프트: {melody_prompts} "
        "저 가사와 멜로디 프롬프트로 노래 제목을 하나 만들어줘 "
        "최소 1단어, 최대 5단어 이내로 제목을 작성해줘. 제목만 한 문장으로 출력하고 다른 말은 절대 하지마"
    )
    title = model.generate_content(prompt).text

    return title

# suno - 노래 만들기
def generate_song(lyrics_prompt, melody_prompt, title):
    # url = "https://apibox.erweima.ai/api/v1/generate"
    #
    # payload = json.dumps({
    #     "prompt": lyrics_prompt,
    #     "style": melody_prompt,
    #     "title": title,
    #     "customMode": True,
    #     "instrumental": False,
    #     "model": "V4_5",
    #     "callBackUrl": "https://your-api.com/music-callback"
    # })
    #
    # headers = {
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json',
    #     'Authorization': 'Bearer ' + TOKEN
    # }
    # response = requests.request("POST", url, headers=headers, data=payload).text
    #
    # print(response)

    id = "6279102da0df35f950a30364904449e7"
    # id = json.loads(response)["data"]["taskId"]
    print(id)
    return id

# suno - 아아디로 노래 정보 조호ㅣ
def get_song_info_by_id(id):
    url = f"https://apibox.erweima.ai/api/v1/generate/record-info?taskId={id}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(response.text)["data"]
    print(response)

    return response

def get_lyrics_id_by_task_id(task_id):
    url = f"https://apibox.erweima.ai/api/v1/lyrics/record-info?taskId={task_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    response = requests.get(url, headers=headers)
    response = json.loads(response.text)

    return response