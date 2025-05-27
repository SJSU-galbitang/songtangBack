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