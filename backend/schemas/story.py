from pydantic import BaseModel

class StoryRequest(BaseModel):
    title: str
    genre: str
    outline: str

class StoryResponse(BaseModel):
    story: str
