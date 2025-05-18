import os

from dotenv import load_dotenv
from google.generativeai import genai

import requests
import json

client = genai.Client(api_key="AIzaSyAFnfVMydG1Sx7Y0AQl6dzRsz7OtkgoxPo")

load_dotenv()
TOKEN = os.getenv("TOKEN")

def analyze_emotion(emotion):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"{emotion} 라는 문장에서 나타나는 감정이 sadness, anger, calm, excitement, hope, love, anxiety, joy 중에서 어디에 속하는지 2개의 키워드로 알려줘. 다른말 하지말고 두개의 키워드만 콤마로 구분해서 알려줘"]
    )

    return response.text.replace("\n", "").split(", ")

def generate_lyrics_prompt(emotion):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            f"{emotion}  라는 감정을 느끼고 있는 사람이 공감할 수 있을만한 노래 가사를 위한 프롬프트 10개 만들어줘 다른 말은 하지말고 프롬프트만 10개 줘 너가 만든 프롬프트를 이용해서 수노를 이용해 노래 가사를 작성할거야. 좀 더 구체적으로 적어줘. 사용자의 감정에 맞는 노래 가사를 알아낼거야. 예시는 필요없어. 다양한 스타일을 표현해줘. 사용자의 감정도 좋지만 사용자가 선호하는 가사 스타일을 찾는데 초점을 맞춰줘. 그냥 다른 문자 없이 한줄로 적어줘. 앞에 숫자하고 . 만 붙여 그리고 영어로 써줘"]
    )

    import re

    result = response.text
    lyrics = re.sub(r'[\n",\d*]', '', result).split(".")
    lyrics = [line.strip() for line in lyrics if line.strip() != ""]
    print("prompt")

    return {
        "lyrics" : lyrics
    }

def generate_lyrics(emotion):
    print("generate")

    prompts = generate_lyrics_prompt(emotion)

    lyrics_ids = []

    # 프롬프트로 가사 만들기 - taskid
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

        response = json.loads(requests.request("POST", url, headers=headers, data=payload).text)

        temp = response["data"]["taskId"]

        if temp == "data":
            print(response)
            continue

        lyrics_ids.append(temp)
        print(response)

    return {"lyrics": lyrics_ids}

def get_lyric(lyrics_id):

    url = f"https://apibox.erweima.ai/api/v1/lyrics/record-info?taskId={lyrics_id}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    import random
    value = random.randint(0, 1)

    try:
        result = response["data"]["response"]["data"][value]["text"]
        return result
    except Exception as e:
        print("가사가 아직 완성되지 않았습니다", e)
        return None

def generate_lyrics_prompt_by_id(lyrics_id: str):
    url = f"https://apibox.erweima.ai/api/v1/lyrics/record-info?taskId={lyrics_id}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + TOKEN
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    try:
        result = json.loads(response["data"]["param"])["prompt"]
        return result
    except Exception as e:
        print("가사가 아직 완성되지 않았습니다", e)
        return None