from Project.songtangBack.data import song as data

def get_song_by_id(song_id: str) -> dict:
    print("song", song_id, "service")

    id, title, length = data.get_song_by_id(song_id)

    length = f"{int(float(length) // 60):02}:{int(float(length) % 60):02}"

    return {
        "id" : id,
        "title" : title,
        "length" : length
    }