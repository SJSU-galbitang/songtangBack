from typing import List

from songtangBack.data import db_connect
from sqlalchemy import create_engine, text

def get_song_by_id(song_id: str):
    engine = create_engine(db_connect.DATABASE_URL, echo=True)
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id, title, length FROM sample_songs WHERE id = :id"),
                {"id": song_id}
            ).fetchone() or {"message" : "해당 아이디의 노래는 존재하지 않습니다."}

            print("✅ 쿼리 실행 성공")
            return result
    except Exception as e:
        print("❌ 쿼리 실행 실패:", e)
        return None

def get_all_song():
    engine = create_engine(db_connect.DATABASE_URL, echo=True)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM sample_songs")).fetchall()
            print("✅ 쿼리 실행 성공")
            return result
    except Exception as e:
        print("❌ 쿼리 실행 실패:", e)
        return None

def get_song_by_emotion(emotion = List[str]):

    import random

    value = random.randint(0, 1)

    _data = get_all_song()
    selected_data = [data for data in _data if data[3] in emotion]
    selected_data = [selected_data[i] for i in range(value, 40, 2)]

    for i in range(20):
        data = selected_data[i]
        temp = {
            "id" : data[0],
            "title" : data[1],
            "length": f"{int(float(data[2]) // 60):02}:{int(float(data[2]) % 60):02}"
        }
        selected_data[i] = temp

    return {
        "melodies" : selected_data
    }

def insert_song(id, title, length, emotion):
    engine = create_engine(db_connect.DATABASE_URL, echo=True)
    try:
        with engine.connect() as conn:
            trans = conn.begin()
            conn.execute(
                text("INSERT INTO sample_songs (id, title, length, emotion) VALUES (:id, :title, :length, :emotion)"),
                {"id": id, "title": title, "length": length, "emotion" : emotion}
            )
            trans.commit()
            print("✅ 쿼리 실행 성공")
    except Exception as e:
        print("❌ 쿼리 실행 실패:", e)


def get_song_prompt_by_id(melody_id):
    engine = create_engine(db_connect.DATABASE_URL, echo=True)
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT prompt, style FROM where id = :id"),{"id" : melody_id}
            ).fetchone()
            print("✅ 쿼리 실행 성공")
            return result
    except Exception as e:
        print("❌ 쿼리 실행 실패:", e)
        return None