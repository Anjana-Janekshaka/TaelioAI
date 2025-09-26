# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import routes
from api import story_writer_routes
from api import story_editor_routes  ## story_editor

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="TaelioAI Story Writer API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(story_writer_routes.router, prefix="/story", tags=["Story Writer"])
app.include_router(story_editor_routes.router, prefix="/story_editor", tags=["Story Editor"])

@app.get("/")
async def root():
    return {"message": "TaelioAI Story Writer API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
