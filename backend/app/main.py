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
from api.routes import multi_agent_workflow as multi_agent_routes
from api.routes import provider_management as provider_routes
from api.routes import admin as admin_routes
from api.routes import user as user_routes
from auth.routes import router as auth_routes
from metrics.usage import UsageLoggingMiddleware
from metrics.prom import create_metrics_response

# Load environment variables from .env file
load_dotenv()

# Check if required environment variables are set
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable is not set!")
    print("Please create a .env file in the backend directory with your Google API key.")
else:
    print(f"[OK] GEMINI_API_KEY loaded successfully: {api_key[:10]}...")
    print(f"Environment variable length: {len(api_key)}")

app = FastAPI(title="TaelioAI Story Writer API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Usage logging middleware (basic)
app.add_middleware(UsageLoggingMiddleware)

# Include all routers
app.include_router(auth_routes, prefix="/auth", tags=["Authentication"])
app.include_router(story_routes.router, prefix="/story", tags=["Story Writer"])
app.include_router(idea_routes.router, prefix="/idea", tags=["Idea Generator"])
app.include_router(workflow_routes.router, prefix="/workflow", tags=["Legacy Workflow"])
app.include_router(multi_agent_routes.router, prefix="/multi-agent", tags=["Multi-Agent System"])
app.include_router(provider_routes.router, prefix="/providers", tags=["Provider Management"])
app.include_router(user_routes.router, prefix="/user", tags=["User"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "TaelioAI Multi-Agent Story Generation API is running!",
        "version": "1.0.0",
        "agents": ["Idea Generator", "Story Writer"],
        "endpoints": {
            "idea_generator": "/idea/generate-idea",
            "story_writer": "/story/write-story", 
            "legacy_workflow": "/workflow/generate-full-story",
            "multi_agent_workflow": "/multi-agent/orchestrated-workflow",
            "system_status": "/multi-agent/system-status",
            "provider_management": "/providers/available"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return create_metrics_response()
