from typing import List

from fastapi import FastAPI, Body, HTTPException

from error import SQLError, InvalidGeminiResponseException, InvalidEmotionResultException, InsufficientInputDataException, IdNotFoundException
from service import song_search as search
from service import song_generation as generate
from service import song_analysis as analyze
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

@app.get("/song/{song_id}")
def get_song_by_id(song_id: str) -> dict:
    try:
        result = search.get_song_by_id(song_id)
        return result
    except IdNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.msg)

@app.get("/lyrics/{lyrics_id}")
def get_lyrics_by_id(lyrics_id):
    try:
        result = search.get_lyrics_by_id(lyrics_id)
        return result
    except IdNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.msg)

@app.get("/survey")
def analyze_emotion(emotion):
    try:
        return analyze.analyze_emotion(emotion)
    except InvalidEmotionResultException as e:
        raise HTTPException(status_code=500, detail=e.msg)
    except SQLError as e:
        raise HTTPException(status_code=500, detail=e.msg)
    except InvalidGeminiResponseException as e:
        raise HTTPException(status_code=500, detail=e.msg)

@app.post("/song")
def generate_song(melody_ids: List[str] = Body(embed = True), lyrics_ids: List[str] = Body(embed = True)):
    try:
        return generate.generate_song(melody_ids, lyrics_ids)
    except InsufficientInputDataException as e:
        raise HTTPException(status_code=422, detail=e.msg)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)