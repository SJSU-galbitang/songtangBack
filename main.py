from typing import List

from fastapi import FastAPI, Body, HTTPException

from Project.songtangBack.error import IdNotFoundException
from service import song as service
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# 허용할 origin 목록
origins = [
    "https://songtang.vercel.app/",
    "https://songtang.vercel.app",
    "http://localhost:5173"

]

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/melody/{melody_id}")
def get_melody_by_id(melody_id: str) -> dict:
    # 에러
    # 해당 아이디의 음악을 찾을 수 없을 때
    try:
        result = service.get_melody_by_id(melody_id)
        return result
    except IdNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.msg)

@app.get("/lyrics/{lyrics_id}")
def get_lyrics_by_id(lyrics_id):
    # 에러
    # 해당 아이디의 음악을 찾을 수 없을 때
    try:
        result = service.get_lyrics_by_id(lyrics_id)
        return result
    except IdNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.msg)

@app.get("/survey")
def analyze_emotion(emotion):
    # 에러
    #
    return service.analyze_emotion(emotion)

@app.post("/song")
def generate_song(melody_ids: List[str] = Body(embed = True), lyrics_ids: List[str] = Body(embed = True)):
    return service.generate_song(melody_ids, lyrics_ids)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)