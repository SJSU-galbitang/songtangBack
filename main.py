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
        return search.get_lyrics_by_task_id(lyrics_id)
    except IdNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.msg)

@app.get("/survey/full")
async def get_full_analysis(emotion: str):
    try:
        ai_emotion = analyze.process_emotion(emotion)

        import asyncio
        melodies_task = asyncio.to_thread(analyze.get_melodies_by_analysis_emotion, ai_emotion)
        lyrics_task = analyze.process_lyrics_async(ai_emotion)  # 이미 async면 OK

        melodies, lyrics = await asyncio.gather(melodies_task, lyrics_task)

        if len(melodies["melodies"]) != 20:
            raise SQLError("멜로디 20개가 아님")
        if len(lyrics["lyrics"]) != 10:
            raise InvalidGeminiResponseException("가사 10개가 아님")

        return {
            "melodies": melodies["melodies"],
            "lyrics": lyrics["lyrics"]
        }

    except (InvalidEmotionResultException, SQLError, InvalidGeminiResponseException) as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/song")
def generate_song(melody_ids: List[str] = Body(embed = True), lyrics_ids: List[str] = Body(embed = True)):
    try:
        return generate.generate_song(melody_ids, lyrics_ids)
    except InsufficientInputDataException as e:
        raise HTTPException(status_code=422, detail=e.msg)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)