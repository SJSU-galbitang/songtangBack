import time

from data import song as data
from ai import song_suno as suno
from ai import song_gemini as gemini
from service import song_search as search

from error import InsufficientInputDataException, SQLError, InvalidGeminiResponseException, InvalidEmotionResultException

def generate_song(melody_ids, lyrics_ids):

    if len(melody_ids) != 10:
        raise InsufficientInputDataException(msg=f"멜로디 아이디가 {len(melody_ids)} 개 왔습니다. 멜로디 아이디는 10개 필요합니다.")
    if len(lyrics_ids) != 5:
        raise InsufficientInputDataException(msg=f"가사 아이디가 {len(lyrics_ids)} 개 왔습니다. 가사 아이디는 10개 필요합니다.")

    lyrics_prompts = []
    for lyrics_id in lyrics_ids:
        lyrics_prompts.append(suno.get_lyrics_prompt_by_id(lyrics_id))
    lyrics_prompt = gemini.generate_one_lyrics_prompt(lyrics_prompts)
    lyrics_task_id = suno.generate_lyrics(lyrics_prompt)["data"]["taskId"]

    melody_info = data.get_melody_info_by_id(melody_ids)
    melody_params = [prompt + style for prompt, style, _ in melody_info]
    melody_prompt = gemini.generate_one_melody_prompt(melody_params)

    time.sleep(2)
    response = suno.get_lyrics(lyrics_task_id)["data"]

    for i in range(10):
        print("\n\nlyrics\n")
        print(response)
        if response["response"] is not None and response["response"]["data"] is not None and response["response"]["data"][0]["text"] is not None and response["response"]["data"][0]["title"] is not None:
            break
        else:
            print("response is None", i)
            time.sleep(2)

        response = suno.get_lyrics(lyrics_task_id)["data"]

    import random
    value = random.randint(0, 1)
    lyrics = response["response"]["data"][value]["text"]
    title = response["response"]["data"][value]["title"]

    id = suno.generate_song(lyrics, melody_prompt, title)

    time.sleep(10)
    response = suno.get_song_info_by_id(id)
    for i in range(6):

        if response["response"] is not None and response["response"]["sunoData"] is not None and response["response"]["sunoData"][0]["id"] is not None:
            break
        else:
            print("response is None", i)
            time.sleep(10)
        response = suno.get_song_info_by_id(id)

    emotion = max([emotion for _, _, emotion in melody_info])
    id = response['response']["sunoData"][0]['id']
    # length = response['response']["sunoData"][value]["duration"]
    # length = f"{int(float(length) // 60):02}:{int(float(length) % 60):02}"
    print("\n\nsonginto\n")
    print(id, title, "00:00", emotion)

    data.insert_data(id, title, "00:00", emotion)

    return {
        "id" : id,
        "title" : title,
        "length" : "00:00"
    }