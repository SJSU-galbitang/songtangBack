from . import db_connect
from sqlalchemy import create_engine, text

def get_song_by_id(song_id: str):
    engine = create_engine(db_connect.DATABASE_URL, echo=True)
    try:
        with engine.connect() as conn:
            print(f"song_id : {song_id} data")
            result = conn.execute(
                text("SELECT id, title, length FROM sample_songs WHERE id = :id"),
                {"id": song_id}
            ).fetchone()

            print("✅ 쿼리 실행 성공")
            return result
    except Exception as e:
        print("❌ 쿼리 실행 실패:", e)
        return None

def get_song_by_id_for_BE(song_id: str):
    engine = create_engine(db_connect.DATABASE_URL, echo=True)
    try:
        with engine.connect() as conn:
            print(f"song_id : {song_id} data")
            result = conn.execute(
                text("SELECT * FROM sample_songs WHERE id = :id"),
                {"id": song_id}
            ).fetchone()

            print("✅ 쿼리 실행 성공")
            return result
    except Exception as e:
        print("❌ 쿼리 실행 실패:", e)
        return None