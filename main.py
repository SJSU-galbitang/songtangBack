from typing import List

from fastapi import FastAPI, Body, HTTPException

from error import IdNotFoundException
from service import song as service
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# 허용할 origin 목록
origins = [
    "https://songtang.vercel.app/",
    "https://songtang.vercel.app",
    "http://localhost:5173",
    "http://10.129.59.129:5173"

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
    # return service.analyze_emotion(emotion)
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
            "820ae873b56b18146eb12b495dbfd06e",
            "10dec08a91f56df01e31cf548c3b0512",
            "dca6697bee49ef816af4106c3c3f251f",
            "0631effe339203dab0a3954041852f98",
            "a0b86564364114f3a9561563bc9a8a84",
            "e5b453613efa553313a5b2152f85d786",
            "9a2b7762a1448394da8846ecdc71e134",
            "273d1bc4c8893cf9bb2559f6ada60356",
            "25aafc7a344c4c314578e27d8c556dbe",
            "34dabdf52f08f6841f7af7ff649d7d7a"
        ]
    }

@app.post("/song")
def generate_song(melody_ids: List[str] = Body(embed = True), lyrics_ids: List[str] = Body(embed = True)):
    return service.generate_song(melody_ids, lyrics_ids)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)