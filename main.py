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

@app.get("/survey")
def get_full_analysis(emotion: str):
    return {
    "melodies": [
        {
            "id": "01e3e959-2994-4b1d-acf7-e883a88ab884",
            "title": "Hopeful Steps",
            "length": "02:57"
        },
        {
            "id": "08a5733b-0a02-4ad6-a2be-b592c4c203c9",
            "title": "Rising Light",
            "length": "04:20"
        },
        {
            "id": "15c4b64c-49cc-421c-b0bf-ac6be06a5e5e",
            "title": "Beyond the Clouds",
            "length": "03:30"
        },
        {
            "id": "1cc18eeb-3fe6-42b0-a115-0c08e9a042eb",
            "title": "Jumpstart",
            "length": "02:52"
        },
        {
            "id": "20e6d083-fcd0-483e-a328-2216fb1b2de3",
            "title": "Ignite",
            "length": "03:34"
        },
        {
            "id": "28586910-cdd5-482a-b966-db67fdb25959",
            "title": "Heart Racer",
            "length": "04:09"
        },
        {
            "id": "420b01e9-bef7-427c-95b1-3922ff7ac65f",
            "title": "New Dawn",
            "length": "03:04"
        },
        {
            "id": "49e24b99-c994-492a-8ad3-cd9b35abf209",
            "title": "Spark Ignition",
            "length": "02:58"
        },
        {
            "id": "614afd79-c6f3-4c89-980f-08902cd4f511",
            "title": "Path Forward",
            "length": "03:46"
        },
        {
            "id": "664f1e06-f897-4b0a-b2c6-1c5635373fda",
            "title": "Charge Up",
            "length": "02:25"
        },
        {
            "id": "6a086b74-fde6-4232-b5ef-77bb77243a63",
            "title": "Bright Sparks",
            "length": "03:30"
        },
        {
            "id": "774b73da-7736-4d6c-be3a-73368ab69039",
            "title": "High Voltage",
            "length": "03:49"
        },
        {
            "id": "8b0ca8cb-c51a-465a-8f9c-12ec82301a78",
            "title": "Brighter Tomorrow",
            "length": "04:07"
        },
        {
            "id": "8e3d48b6-0079-4dfc-b146-7bb5b82e3e5b",
            "title": "Brighter Tomorrow",
            "length": "01:36"
        },
        {
            "id": "a281306f-957d-47d1-96f0-1d56ecf30297",
            "title": "New Horizons",
            "length": "03:36"
        },
        {
            "id": "b84bb799-3de5-492f-a121-d386c1972606",
            "title": "Sunrise Promise",
            "length": "03:19"
        },
        {
            "id": "bb74b984-96e0-4462-8777-d087631aca7a",
            "title": "Path Forward",
            "length": "03:31"
        },
        {
            "id": "c6ffb6c9-94af-4cd9-8700-14cb792adfe6",
            "title": "Rush Hour",
            "length": "03:24"
        },
        {
            "id": "e036e60f-82a6-48ab-b266-9406f7f316f4",
            "title": "Sunrise Promise",
            "length": "03:31"
        },
        {
            "id": "ed271919-e579-43a3-8a98-abfeb77c81f2",
            "title": "Charge Up",
            "length": "02:09"
        }
    ],
    "lyrics": [
        "83193f75c503b4c8a3b618d3d29ce56e",
        "89f4b46a6d68719c73146eee7108bbd4",
        "c22e3239fbd51ea36b882e0c231f66d9",
        "42cf55969b53560f95e5842107d5c805",
        "604536feb0ca2853515b1857f02d27fa",
        "b57a537e63b50a14277c4da8e037cdba",
        "99e88813771bf8b8ac851292db22e0dc",
        "6939257aaf4150bf1aa159cbc5947f9a",
        "3022a1cebb876798c55664e50221a471",
        "2d331356bd3e50f227c0ca714df8a3b1"
    ]
}
    # try:
    #     ai_emotion = analyze.process_emotion(emotion)
    #
    #     import asyncio
    #     melodies_task = asyncio.to_thread(analyze.get_melodies_by_analysis_emotion, ai_emotion)
    #     lyrics_task = analyze.process_lyrics_async(ai_emotion)  # 이미 async면 OK
    #
    #     melodies, lyrics = await asyncio.gather(melodies_task, lyrics_task)
    #
    #     if len(melodies["melodies"]) != 20:
    #         raise SQLError("멜로디 20개가 아님")
    #     if len(lyrics["lyrics"]) != 10:
    #         raise InvalidGeminiResponseException("가사 10개가 아님")
    #
    #     return {
    #         "melodies": melodies["melodies"],
    #         "lyrics": lyrics["lyrics"]
    #     }
    #
    # except (InvalidEmotionResultException, SQLError, InvalidGeminiResponseException) as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@app.post("/song")
def generate_song(melody_ids: List[str] = Body(embed = True), lyrics_ids: List[str] = Body(embed = True)):
    # try:
    #     return generate.generate_song(melody_ids, lyrics_ids)
    # except InsufficientInputDataException as e:
    #     raise HTTPException(status_code=422, detail=e.msg)
    # # except Exception as e:
    # #     raise HTTPException(status_code=500, detail=str(e))
    return {
        "id": "7037aaf7-dc2c-409f-8672-514dd71e8386",
        "title": "The Journey Within",
        "length": "03:26"
    }

@app.get("/song/length/{song_id}")
def get_song_duration(song_id):
    return search.get_song_duration(song_id)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)