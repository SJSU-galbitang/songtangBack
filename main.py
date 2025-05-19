from typing import List

from fastapi import FastAPI, Body
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
    allow_origins=origins,            # 허용할 origin 목록
    allow_credentials=True,
    allow_methods=["*"],              # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],              # 모든 헤더 허용
)

@app.get("/song/{song_id}")
def get_song_by_id(song_id: str) -> dict:
    return service.get_song_by_id(song_id)

@app.get("/lyrics/{song_id}")
def get_lyrics_by_id(song_id: str):
    return service.get_lyrics_by_id(song_id)

@app.get("/survey")
def analyze_emotion(emotion):
    return service.analyze_emotion(emotion)

@app.post("/song")
def generate_song(melody_ids: List[str] = Body(embed = True), lyrics_ids: List[str] = Body(embed = True)):
    return service.generate_song(melody_ids, lyrics_ids)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)