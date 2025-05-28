from data import song as data
from ai import song_suno as suno

import time

def get_song_by_id(song_id):
    id, title, length = data.get_song_by_id(song_id)

    return {
        "id" : id,
        "title" : title,
        "length" : length
    }

def get_lyrics_by_task_id(task_id):
    response = suno.get_lyrics(task_id)
    import random
    value = random.randint(0, 1)

    print(response)

    result = response["data"]["response"]["data"][value]["text"]
    title = response["data"]["response"]["data"][value]["title"]
    print(result)
    return {
        "lyrics" : result,
        "title" : title
    }


def get_song_duration(song_id):
    time.sleep(1)
    response = suno.get_song_info_by_id(id)
    for i in range(6):
        print(response)
        if response is not None and response["response"] is not None and response["response"]["sunoData"] is not None and response["response"]["sunoData"][0]["id"] is not None:
            length = response['response']["sunoData"][0]["duration"]
            length = f"{int(float(length) // 60):02}:{int(float(length) % 60):02}"
            data.update_duration(song_id, length)
            return {"length": length}
        else:
            print("response is None", i)
            time.sleep(1)
        response = suno.get_song_info_by_id(id)
    return {"length": "00:00"}