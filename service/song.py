from data import song as data
from ai import song as ai

def get_song_by_id(song_id: str) -> dict:

    result = data.get_song_by_id(song_id)
    if type(result) == dict:
        return result

    id, title, length = data.get_song_by_id(song_id)
    length = f"{int(float(length) // 60):02}:{int(float(length) % 60):02}"

    return {
        "id" : id,
        "title" : title,
        "length" : length
    }


def analyze_emotion(emotion):
    ai_emotion = ai.analyze_emotion(emotion)
    melodies = data.get_song_by_emotion(ai_emotion)
    print("success 1")
    lyrics = ai.generate_lyrics(emotion)
    print("success 2")
    return [melodies, lyrics]


def get_lyrics_by_id(song_id):
    return {"lyrics" : ai.get_lyric(song_id)}

def generate_song(melody_ids, lyrics_ids):

    lyrics_prompts = []
    for lyrics_id in lyrics_ids:
        lyrics_prompts.append(ai.generate_lyrics_prompt_by_id(lyrics_id))

    melody_prompts = []
    for melody_id in melody_ids:
        melody_prompts.append(data.get_song_prompt_by_id(melody_id))

    return None