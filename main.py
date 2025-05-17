from fastapi import FastAPI
from Project.songtangBack.service import song as service
app =FastAPI()

@app.get("/song/{song_id}")
def get_song_by_id(song_id: str) -> dict:
    print("main", song_id)
    return service.get_song_by_id(song_id)

@app.get("/survey")
def analyze_emotion(emotion) -> list:
    return service.analyze_emotion(emotion)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)