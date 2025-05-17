from uuid import uuid4
from fastapi import HTTPException
from uuid import uuid4
from fastapi import HTTPException
from model.song_request import SongCreateRequest, SongCreateResponse
from fastapi import FastAPI
from service import song as service

app = FastAPI()

@app.get("/song/{song_id}")
def get_song_by_id(song_id: str) -> dict:
    print("main", song_id)
    return service.get_song_by_id(song_id)


# 클라우드에서 받아온 노래 데이터를 서버에서 제공하는 API 엔드포인트
@app.post("/song", response_model=SongCreateResponse)
def provide_song_endpoint(request: SongCreateRequest):
    if len(request.melodies) != 10:
        raise HTTPException(status_code=400, detail="melodies must contain exactly 10 items")
    if len(request.lyrics) != 5:
        raise HTTPException(status_code=400, detail="lyrics must contain exactly 5 items")

    song_id = str(uuid4())
    title = f"song_{song_id[:8]}"
    length = "05:23"  # 실제 길이는 클라우드 데이터 기반으로 변경 가능

    return SongCreateResponse(
        id=song_id,
        title=title,
        length=length
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)