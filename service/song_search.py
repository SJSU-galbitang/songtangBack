from data import song as data
from ai import song_suno as suno

def get_song_by_id(song_id):
    id, title, length = data.get_song_by_id(song_id)

    return {
        "id" : id,
        "title" : title,
        "length" : length
    }

def get_lyrics_id_by_task_id(task_id):
    response = suno.get_lyrics_id_by_task_id(task_id)
    print(response)

    import random
    value = random.randint(0, 1)

    return response["data"]["response"]["data"][value]["id"]

def get_lyrics_by_id(task_id):
    lyrics_id = get_lyrics_id_by_task_id(task_id)
    response = suno.get_lyrics(lyrics_id)
    import random
    value = random.randint(0, 1)

    print(response)

    result = response["data"]["response"]["data"][value]["text"]
    print(result)
    return {"lyrics" : result}