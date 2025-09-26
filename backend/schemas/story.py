from pydantic import BaseModel

# Story Writer Schemas
class StoryRequest(BaseModel):
    title: str
    genre: str
    outline: str

class StoryResponse(BaseModel):
    story: str
