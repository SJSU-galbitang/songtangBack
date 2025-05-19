from data import song as data
from ai import song as ai

def get_melody_by_id(melody_id):

    id, title, length = data.get_melody_by_id(melody_id)
    length = f"{int(float(length) // 60):02}:{int(float(length) % 60):02}"

    return {
        "id" : id,
        "title" : title,
        "length" : length
    }

def get_lyrics_by_id(song_id):
    return {"lyrics" : ai.get_lyrics(song_id)}

def analyze_emotion(emotion):
    ai_emotion = ai.analyze_emotion(emotion)
    melodies = data.get_song_by_emotion(ai_emotion)
    lyrics = ai.generate_lyrics(emotion)
    return {
        "melodies" : melodies,
        "lyrics" : lyrics
    }

def generate_song(melody_ids, lyrics_ids):

    lyrics_prompts = []
    for lyrics_id in lyrics_ids:
        lyrics_prompts.append(ai.generate_lyrics_prompt_by_id(lyrics_id))

    melody_info = data.get_melody_info_by_id(melody_ids)
    melody_prompts = [prompt for prompt, _, _ in melody_info]
    melody_style = [style for _, style ,_ in melody_info]
    melody_emotion = max([emotion for _, _, emotion in melody_info])

    return ai.generate_one_song(lyrics_prompts, melody_prompts + melody_style, melody_emotion)
