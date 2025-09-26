from pydantic import BaseModel
from typing import Optional

class IdeaRequest(BaseModel):
    prompt: str
    genre: Optional[str] = None
    tone: Optional[str] = None

class IdeaResponse(BaseModel):
    title: str
    genre: str
    outline: str
    characters: Optional[str] = None
    setting: Optional[str] = None
