from typing import List

from data import db_connect
from sqlalchemy import create_engine, text

from error import IdNotFoundException

engine = create_engine(db_connect.DATABASE_URL, echo=True)

def get_melody_by_id(melody_id: str):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, title, length FROM songs WHERE id = :id"),
        {"id": melody_id}
        ).fetchone()

        if result is None:
            raise IdNotFoundException(msg="해당 아이디에 대한 멜로디 정보를 찾을 수 없습니다.")

        return result

def get_all_song():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, emotion, title, length FROM sample_songs")).fetchall()
            print("✅ 쿼리 실행 성공")
            return result
    except Exception as e:
        print("❌ 쿼리 실행 실패:", e)
        return None

def get_song_by_emotion(emotion = List[str]):
    import random
    value = random.randint(0, 1)

    _data = get_all_song()
    selected_data = [data for data in _data if list(data)[1] in emotion]
    print(len(selected_data))
    selected_data = [selected_data[i] for i in range(value, len(selected_data), 2)]

    for i in range(20):
        data = selected_data[i]
        temp = {
            "id" : data[0],
            "title" : data[2],
            "length": f"{int(float(data[3]) // 60):02}:{int(float(data[3]) % 60):02}"
        }
        selected_data[i] = temp

    return selected_data

def get_melody_info_by_id(melody_ids):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT prompt, style, emotion FROM sample_songs where id in :id"),{"id" : melody_ids}
            ).fetchall()
            print("✅ 쿼리 실행 성공")

            return result
    except Exception as e:
        print("❌ 쿼리 실행 실패:", e)
        return None

def insert_data(id, title, length, emotion):
    try:
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                conn.execute(
                    text(
                        "INSERT INTO songs (id, title, length, emotion) VALUES (:id, :title, :length, :emotion)"),
                    {"id": id, "title": title, "length": length, "emotion": emotion}
                )
                trans.commit()
                print("✅ 쿼리 실행 성공")
            except Exception as inner_e:
                trans.rollback()
                print("❌ 트랜잭션 실패, 롤백:", inner_e)
    except Exception as e:
        print("❌ 연결 또는 트랜잭션 시작 실패:", e)