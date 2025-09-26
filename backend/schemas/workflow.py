from pydantic import BaseModel
from typing import Optional
from .idea import IdeaResponse

class FullStoryRequest(BaseModel):
    prompt: str
    genre: Optional[str] = None
    tone: Optional[str] = None

class FullStoryResponse(BaseModel):
    idea: IdeaResponse
    story: str
