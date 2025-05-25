from data import db_connect
from sqlalchemy import create_engine, text

from error import IdNotFoundException, SQLError

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
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, emotion, title, length FROM sample_songs")).fetchall()
        print("✅ 쿼리 실행 성공")

        if result == []:
            raise SQLError(msg="sample_songs 테이블에 저장된 값이 없습니다.")

        return result

def get_melody_info_by_id(melody_ids):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT prompt, style, emotion FROM sample_songs where id in :id"),{"id" : melody_ids}
        ).fetchall()
        print("✅ 쿼리 실행 성공")

        if len(result) != len(melody_ids):
            raise SQLError(msg=f"제공하신 멜로디 아이디 {len(melody_ids)} 개 중 {len(result)} 만 유효합니다.")

        return result

def insert_data(id, title, length, emotion):
    with engine.connect() as conn:
        trans = conn.begin()
        conn.execute(
                text(
                    "INSERT INTO songs (id, title, length, emotion) VALUES (:id, :title, :length, :emotion)"),
                {"id": id, "title": title, "length": length, "emotion": emotion}
        )
        trans.commit()
        print("✅ 쿼리 실행 성공")