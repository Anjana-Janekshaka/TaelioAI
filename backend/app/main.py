import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.routes import story as story_routes
from api.routes import idea as idea_routes
from api.routes import workflow as workflow_routes

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

# Include all routers
app.include_router(story_routes.router, prefix="/story", tags=["Story Writer"])
app.include_router(idea_routes.router, prefix="/idea", tags=["Idea Generator"])
app.include_router(workflow_routes.router, prefix="/workflow", tags=["Multi-Agent Workflow"])

@app.get("/")
async def root():
    return {
        "message": "TaelioAI Multi-Agent Story Generation API is running!",
        "version": "1.0.0",
        "agents": ["Idea Generator", "Story Writer"],
        "endpoints": {
            "idea_generator": "/idea/generate-idea",
            "story_writer": "/story/write-story", 
            "full_workflow": "/workflow/generate-full-story",
            "workflow_info": "/workflow/workflow-info"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
