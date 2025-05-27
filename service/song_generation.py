from data import song as data
from ai import song_suno as suno
from ai import song_gemini as gemini

from error import InsufficientInputDataException, SQLError, InvalidGeminiResponseException, InvalidEmotionResultException

def generate_song(melody_ids, lyrics_ids):

    if len(melody_ids) != 10:
        raise InsufficientInputDataException(msg=f"멜로디 아이디가 {len(melody_ids)} 개 왔습니다. 멜로디 아이디는 10개 필요합니다.")
    if len(lyrics_ids) != 5:
        raise InsufficientInputDataException(msg=f"가사 아이디가 {len(lyrics_ids)} 개 왔습니다. 가사 아이디는 10개 필요합니다.")

    lyrics_prompts = []
    for lyrics_id in lyrics_ids:
        lyrics_prompts.append(suno.get_lyrics_prompt_by_id(lyrics_id))
    lyrics_prompt = gemini.generate_one_lyrics(lyrics_prompts)
    lyrics_task_id = suno.generate_lyrics(lyrics_prompt)

    melody_info = data.get_melody_info_by_id(melody_ids)
    melody_params = [prompt + style for prompt, style, _ in melody_info]
    melody_prompt = gemini.generate_one_melody(melody_params)

    title = gemini.generate_title(lyrics_prompt, melody_prompt)

    id = suno.generate_song(lyrics_prompt, melody_prompt, title)
    # id = "9fadc597-c8ad-4b86-8cea-a832d2651a31"

    emotion = max([emotion for _, _, emotion in melody_info])

    response = suno.get_song_info_by_id(id)

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