from pydantic import BaseModel
from typing import Optional

# Story Writer Schemas
class StoryRequest(BaseModel):
    title: str
    genre: str
    outline: str
    tone: Optional[str] = None
    characters: Optional[str] = None
    setting: Optional[str] = None

class StoryResponse(BaseModel):
    story: str
