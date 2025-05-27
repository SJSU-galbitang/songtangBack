import os
import json
import requests
from dotenv import load_dotenv

from data import song as data

from error import IdNotFoundException, InvalidEmotionResultException

load_dotenv()
TOKEN = os.getenv("TOKEN")

# suno - 가사 생성
def generate_lyrics(prompt):
    url = "https://apibox.erweima.ai/api/v1/lyrics"

    payload = json.dumps({
        "prompt": prompt + "영어로 해줘",
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

# 태스크아이디로 가사 아이디 조회
def get_lyrics_id_by_task_id(task_id):
    url = f"https://apibox.erweima.ai/api/v1/lyrics/record-info?taskId={task_id}"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    response = requests.get(url, headers=headers)
    response = json.loads(response.text)

    return response

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

# suno - 노래 만들기
def generate_song(lyrics, melody_prompt, title):
    print(lyrics)
    url = "https://apibox.erweima.ai/api/v1/generate"

    payload = json.dumps({
        "prompt": lyrics,
        "style": melody_prompt,
        "title": title,
        "customMode": True,
        "instrumental": False,
        "model": "V4_5",
        "callBackUrl": "https://your-api.com/music-callback"
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.request("POST", url, headers=headers, data=payload).text

    print(response)

    # id = "6279102da0df35f950a30364904449e7"
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