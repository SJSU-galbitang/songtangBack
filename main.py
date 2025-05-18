from typing import List

from fastapi import FastAPI, Body
from Project.songtangBack.service import song as service
app =FastAPI()

@app.get("/song/{song_id}")
def get_song_by_id(song_id: str) -> dict:
    return service.get_song_by_id(song_id)

@app.get("/lyrics/{song_id}")
def get_lyrics_by_id(song_id: str) -> dict:
    return service.get_lyrics_by_id(song_id)

@app.get("/survey")
def analyze_emotion(emotion) -> list:
    return service.analyze_emotion(emotion)

@app.post("/song")
def generate_song(melody_ids: List[str] = Body(embed = True), lyrics_ids: List[str] = Body(embed = True)):
    return service.generate_song(melody_ids, lyrics_ids)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)