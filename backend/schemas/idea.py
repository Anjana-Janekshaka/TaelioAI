from pydantic import BaseModel
from typing import Optional, List

class IdeaRequest(BaseModel):
    prompt: str
    genre: Optional[str] = None
    tone: Optional[str] = None

class IdeaResponse(BaseModel):
    title: str
    genre: str
    tone: str
    outline: str
    characters: Optional[List[str]] = None
    setting: Optional[str] = None
