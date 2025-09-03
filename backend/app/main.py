from fastapi import FastAPI
from api import story_writer_routes

app = FastAPI()

app.include_router(story_writer_routes.router, prefix="/story", tags=["Story Writer"])
