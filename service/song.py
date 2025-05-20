import json
from typing import List

from data import song as data
from ai import song as ai

from error import InsufficientInputDataException, SQLError, InvalidGeminiResponseException

from Project.songtangBack.error import InvalidEmotionResultException


def get_song_by_id(song_id):

    id, title, length = data.get_melody_by_id(song_id)
    length = f"{int(float(length) // 60):02}:{int(float(length) % 60):02}"

    return {
        "id" : id,
        "title" : title,
        "length" : length
    }

def get_lyrics_by_id(song_id):
    return {"lyrics" : ai.get_lyrics(song_id)}

def get_song_by_emotion(emotion = List[str]):
    import random
    value = random.randint(0, 1)

    _data = data.get_all_song()
    selected_data = [data for data in _data if list(data)[1] in emotion]
    print(len(selected_data))
    selected_data = [selected_data[i] for i in range(value, len(selected_data), 2)]

    for i in range(20):
        sample = selected_data[i]
        temp = {
            "id" : sample[0],
            "title" : sample[2],
            "length": f"{int(float(sample[3]) // 60):02}:{int(float(sample[3]) % 60):02}"
        }
        selected_data[i] = temp

    return selected_data

def process_emotion(emotion):
    for i in range(5):
        response = ai.analyze_emotion(emotion)
        emotions = {"sadness", "anger", "calm", "excitement", "hope", "love", "anxiety", "joy"}
        ai_emotion = list(map(str.lower, response.text.replace("\n", "").split(", ")))
        result = list(set(ai_emotion) & emotions)

        if len(result) == 2:
            return result

        if i == 4:
            raise InvalidEmotionResultException(msg="제미나이 감정 분석 결과가 잘못되었습니다.")

    return None

def process_lyrics(emotion):
    prompt = ai.generate_lyrics_prompt(emotion)

    import re
    lines = re.split(r'[\n\r]', prompt)
    prompts = [line.split('.', 1)[-1].strip() for line in lines if '.' in line]

    lyrics_ids = []

    for prompt in prompts:
        response = ai.generate_lyrics(prompt)
        task_id = response.get("data", {}).get("taskId")

        if task_id:
            lyrics_ids.append(task_id)
        else:
            print("taskId 없음:", response)

    return lyrics_ids

def analyze_emotion(emotion):
    ai_emotion = process_emotion(emotion)
    melodies = get_song_by_emotion(ai_emotion)
    lyrics = process_lyrics(emotion)

    if len(melodies) != 20:
        raise SQLError(msg=f"멜로디 개수가 20개가 아님 {len(melodies)} 개 입니다")

    if len(lyrics) != 10:
        raise InvalidGeminiResponseException(msg=f"가사 개수가 10개가 아님 {len(lyrics)} 개 입니다")

    return {
        "melodies" : melodies,
        "lyrics" : lyrics
    }

def generate_song(melody_ids, lyrics_ids):

    if len(melody_ids) != 10:
        raise InsufficientInputDataException(msg=f"멜로디 아이디가 {len(melody_ids)} 개 왔습니다. 멜로디 아이디는 10개 필요합니다.")

    if len(lyrics_ids) != 5:
        raise InsufficientInputDataException(msg=f"가사 아이디가 {len(lyrics_ids)} 개 왔습니다. 가사 아이디는 10개 필요합니다.")

    lyrics_prompts = []
    for lyrics_id in lyrics_ids:
        lyrics_prompts.append(ai.get_lyrics_prompt_by_id(lyrics_id))
    lyrics_prompt = ai.generate_one_lyrics(lyrics_prompts)

    melody_info = data.get_melody_info_by_id(melody_ids)
    melody_params = [prompt + style for prompt, style, _ in melody_info]
    melody_prompt = ai.generate_one_melody(melody_params)

    title = ai.generate_title(lyrics_prompt, melody_prompt)

    id = ai.generate_song(lyrics_prompt, melody_prompt, title)

    emotion = max([emotion for _, _, emotion in melody_info])

    # data.insert_data(id, title, "00:00", emotion)

    return ai.get_song_info_by_id(id)
