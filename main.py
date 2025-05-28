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
    except Exception:
        raise HTTPException(status_code=500, detail="노래 완성 안됨")

@app.get("/survey")
def get_full_analysis(emotion: str):
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
    return {
    "melodies": [
                    {
                        "id": "080ae684-b4a6-4fdc-a565-8cc6a14b6a39",
                        "title": "Rising Light",
                        "length": "04:43"
                    },
                    {
                        "id": "12ab525c-54ae-4699-84f8-f502e1b45a5e",
                        "title": "Ignite",
                        "length": "02:34"
                    },
                    {
                        "id": "1bb79dc1-7bc4-4386-9b20-2a724d712f22",
                        "title": "Light Within",
                        "length": "03:41"
                    },
                    {
                        "id": "1e24cae7-7f68-460e-8361-c99d2e0b3309",
                        "title": "Electric Night",
                        "length": "03:44"
                    },
                    {
                        "id": "24fa031b-37fb-4402-84bc-85c721f01d2f",
                        "title": "Light Within",
                        "length": "03:29"
                    },
                    {
                        "id": "3666ce57-a1b1-410f-9746-7d7f1cf4df3c",
                        "title": "Electric Pulse",
                        "length": "03:47"
                    },
                    {
                        "id": "49784f7f-1023-421d-9f01-0df9e653e92b",
                        "title": "Open Skies",
                        "length": "03:01"
                    },
                    {
                        "id": "5a5189e4-0535-4d5c-bf30-6fc64e034f73",
                        "title": "Electric Night",
                        "length": "03:39"
                    },
                    {
                        "id": "6277f97c-be64-43ec-a589-c4b9c49c75b5",
                        "title": "New Dawn",
                        "length": "02:57"
                    },
                    {
                        "id": "68c24fe2-0f24-4cc9-95c6-f7e061066ac9",
                        "title": "Rush Hour",
                        "length": "03:21"
                    },
                    {
                        "id": "7193d20f-7e8e-4c14-8874-cb279b392ec8",
                        "title": "Beyond the Clouds",
                        "length": "02:26"
                    },
                    {
                        "id": "80e6acb2-3fbf-4533-971e-a94d81b8f18a",
                        "title": "Heart Racer",
                        "length": "02:16"
                    },
                    {
                        "id": "8d4bea42-e044-47a0-bf9c-f99f33df8d75",
                        "title": "New Horizons",
                        "length": "03:16"
                    },
                    {
                        "id": "8eb70514-8d91-4ece-82ec-51bc75cf2e1f",
                        "title": "Bright Sparks",
                        "length": "03:23"
                    },
                    {
                        "id": "a5a8fd12-d867-4336-9ece-52196c55f49c",
                        "title": "Jumpstart",
                        "length": "02:23"
                    },
                    {
                        "id": "bae9aca5-264c-4afc-9e09-09c77123ecd6",
                        "title": "Electric Pulse",
                        "length": "02:49"
                    },
                    {
                        "id": "be2444f1-4920-400a-993b-994f4a648119",
                        "title": "High Voltage",
                        "length": "04:18"
                    },
                    {
                        "id": "c921515f-adf4-42d1-a8ee-105f482c9f48",
                        "title": "Open Skies",
                        "length": "03:19"
                    },
                    {
                        "id": "ed1df020-e8cd-4d0d-829d-c0c5d0ff24ac",
                        "title": "Hopeful Steps",
                        "length": "02:34"
                    },
                    {
                        "id": "fd803a85-4c2f-4eac-9212-c891e9811449",
                        "title": "Spark Ignition",
                        "length": "02:54"
                    }
                ],
                "lyrics": [
                    "40f20b5d791db5e4bd85eda52b9dd32f",
                    "dd8f2143bffeaa7a1fd3cc11523cf8fb",
                    "e4b6a517a7ac8196fbad3cc7d2df0759",
                    "0ef2eb455e7a5d7953dcf772059a578c",
                    "8cadafa9db8ba0c5532e0fdc54450d75",
                    "d29b5d98d60cd96c2eb48ab165d9d45c",
                    "363f784ca823dc38de48c8b5f71e5d8e",
                    "79af9590c1e5e966dedaa6a1a859cb84",
                    "e771ff54182d3e42c25c9dab1dff9ab5",
                    "cc88d906f4686555e34dde959e51a70d"
                ]
            }

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