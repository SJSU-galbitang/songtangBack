from pydantic import BaseModel
from typing import List

class SongCreateRequest(BaseModel):
    melodies: List[str]
    lyrics: List[str]

class SongCreateResponse(BaseModel):
    title: str
    id: str
    length: str