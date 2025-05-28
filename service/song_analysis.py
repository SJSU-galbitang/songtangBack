from typing import List
import asyncio

from data import song as data_song
from ai import song_suno as suno
from ai import song_gemini as gemini

from error import InsufficientInputDataException, SQLError, InvalidGeminiResponseException, InvalidEmotionResultException

def process_emotion(emotion):
    for i in range(5):
        import re
        response = gemini.analyze_emotion(emotion)
        emotions = {"sadness", "anger", "calm", "excitement", "hope", "love", "anxiety", "joy"}
        ai_emotion = [e.strip().lower() for e in re.split(r",\s*", response.text.strip())]
        result = list(set(ai_emotion) & emotions)

        if len(result) == 2:
            return result

        if i == 4:
            raise InvalidEmotionResultException(msg="제미나이 감정 분석 결과가 잘못되었습니다.")

    return None

def get_song_by_emotion(emotion = List[str]):
    _data = data_song.get_all_song()
    selected_data = []

    for data in _data:
        if list(data)[1] in emotion:
            selected_data.append({
                "id": data[0],
                "title": data[2],
                "length": f"{int(float(data[3]) // 60):02}:{int(float(data[3]) % 60):02}"
            })

    import random
    value = random.randint(0, 1)

    return [selected_data[i] for i in range(value, len(selected_data), 2)]

def get_melodies_by_analysis_emotion(emotion):
    ai_emotion = process_emotion(emotion)
    melodies = get_song_by_emotion(ai_emotion)

    if len(melodies) != 20:
        raise SQLError(msg=f"멜로디 개수가 20개가 아님 {len(melodies)} 개 입니다")

    return {
        "melodies": melodies
    }

async def process_lyrics_async(emotion):
    gemini_prompt = gemini.generate_lyrics_prompt(emotion)

    import re
    lines = re.split(r'[\n\r]', gemini_prompt)
    prompts = [line.split('.', 1)[-1].strip() for line in lines if '.' in line]

    if len(prompts) != 10:
        raise InvalidGeminiResponseException("제미나이 응답 오류: 가사 프롬프트가 10개가 아님")

    def generate(prompt):
        return suno.generate_lyrics(prompt)  # 동기 함수라고 가정

    tasks = [asyncio.to_thread(generate, p) for p in prompts]
    results = await asyncio.gather(*tasks)

    lyrics_task_ids = []

    for res in results:
        data = res.get("data", {})
        if "taskId" in data:
            lyrics_task_ids.append(data["taskId"])
        else:
            raise InvalidGeminiResponseException("Suno 응답 오류: taskId 없음")

    return {
        "lyrics": lyrics_task_ids
    }