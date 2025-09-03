import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api import story_writer_routes

# Load environment variables from .env file
load_dotenv()

# Check if required environment variables are set
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable is not set!")
    print("Please create a .env file in the backend directory with your Google API key.")
else:
    print(f"✅ GEMINI_API_KEY loaded successfully: {api_key[:10]}...")
    print(f"Environment variable length: {len(api_key)}")

app = FastAPI(title="TaelioAI Story Writer API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(story_writer_routes.router, prefix="/story", tags=["Story Writer"])

@app.get("/")
async def root():
    return {"message": "TaelioAI Story Writer API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
