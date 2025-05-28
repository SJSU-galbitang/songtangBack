import time

from data import song as data
from ai import song_suno as suno
from ai import song_gemini as gemini
from service import song_search as search

from error import InsufficientInputDataException, SQLError, InvalidGeminiResponseException, InvalidEmotionResultException

def wait_for_lyrics_response(task_id, retries=10, delay=2):
    for i in range(retries):
        response = suno.get_lyrics(task_id).get("data", {})
        try:
            result = response["response"]["data"][0]
            if result.get("text") and result.get("title"):
                return result["text"], result["title"]
        except (KeyError, TypeError, IndexError):
            pass

        print("가사 응답 대기 중...", i)
        time.sleep(delay)

    raise InvalidGeminiResponseException("가사 생성 실패: 응답을 받지 못했습니다.")

def wait_for_song_response(song_task_id, retries=10, delay=10):
    song_id = ""
    length = "00:00"
    for i in range(retries):
        response = suno.get_song_info_by_id(song_task_id)
        try:
            result = response["response"]["sunoData"][0]
            song_id = result["id"]
            duration = float(result["duration"])
            length = f"{int(duration // 60):02}:{int(duration % 60):02}"
            return song_id, length
        except (KeyError, TypeError, IndexError, ValueError):
            pass

        print("곡 생성 응답 대기 중...", i)
        time.sleep(delay)

    return song_id, length

def generate_song(melody_ids, lyrics_ids):
    if len(melody_ids) != 10:
        raise InsufficientInputDataException(f"멜로디 아이디가 {len(melody_ids)}개입니다. 10개 필요합니다.")
    if len(lyrics_ids) != 5:
        raise InsufficientInputDataException(f"가사 아이디가 {len(lyrics_ids)}개입니다. 5개 필요합니다.")

    lyrics_prompts = [suno.get_lyrics_prompt_by_id(lid) for lid in lyrics_ids]
    lyrics_prompt = gemini.generate_one_lyrics_prompt(lyrics_prompts)
    lyrics_task_id = suno.generate_lyrics(lyrics_prompt)["data"]["taskId"]

    melody_info = data.get_melody_info_by_id(melody_ids)
    melody_params = [prompt + style for prompt, style, _ in melody_info]
    melody_prompt = gemini.generate_one_melody_prompt(melody_params)

    lyrics, title = wait_for_lyrics_response(lyrics_task_id)

    song_task_id = suno.generate_song(lyrics, melody_prompt, title)
    song_id, length = wait_for_song_response(song_task_id)

    emotion = max([emotion for _, _, emotion in melody_info])
    data.insert_data(song_id, title, length, emotion)

    return {
        "id": song_id,
        "title": title,
        "length": length
    }