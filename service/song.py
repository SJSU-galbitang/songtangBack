from typing import List

from data import song as data
from ai import song as ai

from error import InsufficientInputDataException, SQLError, InvalidGeminiResponseException, InvalidEmotionResultException


def get_song_by_id(song_id):

    id, title, length = data.get_melody_by_id(song_id)

    return {
        "id" : id,
        "title" : title,
        "length" : length
    }

def get_lyrics_by_id(song_id):
    response = ai.get_lyrics(song_id)
    import random
    value = random.randint(0, 1)

    print(response)

    result = response["data"]["response"]["data"][value]["text"]
    print(result)
    return {"lyrics" : result}

def process_emotion(emotion):
    for i in range(5):
        import re
        response = ai.analyze_emotion(emotion)
        emotions = {"sadness", "anger", "calm", "excitement", "hope", "love", "anxiety", "joy"}
        ai_emotion = [e.strip().lower() for e in re.split(r",\s*", response.text.strip())]
        result = list(set(ai_emotion) & emotions)

        if len(result) == 2:
            return result

        if i == 4:
            raise InvalidEmotionResultException(msg="제미나이 감정 분석 결과가 잘못되었습니다.")

    return ["joy", "sadness"]

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

def process_lyrics(emotion):
    prompt = ai.generate_lyrics_prompt(emotion)

    import re
    lines = re.split(r'[\n\r]', prompt)
    prompts = [line.split('.', 1)[-1].strip() for line in lines if '.' in line]

    if len(prompts) != 10:
        raise InvalidGeminiResponseException("제미나이로 부터 정상적인 응답을 받지 못했습니다. : 제공된 노래 가사 프롬프트의 개수가 10개가 아님")

    lyrics_ids = []

    for prompt in prompts:
        response = ai.generate_lyrics(prompt)
        response = response.get("data", {})

        print(response.keys())

        if "taskId" in response:
            task_id = response["taskId"]
            lyrics_response = ai.get_lyrics_id_by_task_id(task_id)
            print(lyrics_response)
            lyrics_response = lyrics_response.get("data", {})
            print(lyrics_response)
            print(type(lyrics_response))

            lyrics_ids.append(0)

        else:
            raise InvalidGeminiResponseException("제미나이로 부터 정상적인 응답을 받지 못했습니다.")

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
    lyrics_task_id = ai.generate_lyrics(lyrics_prompt)

    melody_info = data.get_melody_info_by_id(melody_ids)
    melody_params = [prompt + style for prompt, style, _ in melody_info]
    melody_prompt = ai.generate_one_melody(melody_params)

    title = ai.generate_title(lyrics_prompt, melody_prompt)

    id = ai.generate_song(lyrics_prompt, melody_prompt, title)
    # id = "9fadc597-c8ad-4b86-8cea-a832d2651a31"

    emotion = max([emotion for _, _, emotion in melody_info])

    response = ai.get_song_info_by_id(id)

    import random
    value = random.randint(0, 1)

    id = response['response']["sunoData"][value]['id']
    title = response['response']["sunoData"][value]["title"].replace("\n", "")
    length = response['response']["sunoData"][value]["duration"]
    length = f"{int(float(length) // 60):02}:{int(float(length) % 60):02}"
    # prompt = json.loads(response["param"])["prompt"].replace("\n", "")
    # style = json.loads(response["param"])["style"].replace("\n", "")

    print(id, title, length, emotion)

    data.insert_data(id, title, length, emotion)

    return {
        "id" : id,
        "title" : title,
        "length" : length
    }