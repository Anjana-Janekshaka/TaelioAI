# TaelioAI Multi-Agent System

## Overview
TaelioAI now implements a multi-agent system that follows the flowchart structure:
1. **User Prompt** → **Idea Generator Agent** → **Story Idea**
2. **Story Idea** → **Story Writer Agent** → **Full Story**

## Architecture

### Agents

#### 1. Idea Generator Agent
- **File**: `services/idea_generator.py`
- **API**: `/idea/generate-idea`
- **Purpose**: Takes a simple prompt and generates a detailed story idea
- **Input**: `IdeaRequest` (prompt, genre, tone)
- **Output**: `IdeaResponse` (title, genre, outline, characters, setting)

#### 2. Story Writer Agent (Existing)
- **File**: `services/story_writer.py`
- **API**: `/story/write-story`
- **Purpose**: Takes a story idea and expands it into a full story
- **Input**: `StoryRequest` (title, genre, outline)
- **Output**: `StoryResponse` (story)

### Combined Workflow

#### Full Story Workflow
- **File**: `services/full_story_workflow.py`
- **API**: `/workflow/generate-full-story`
- **Purpose**: Chains Idea Generator + Story Writer
- **Input**: `FullStoryRequest` (prompt, genre, tone)
- **Output**: `FullStoryResponse` (idea + story)

## API Endpoints

### Individual Agents
```
POST /idea/generate-idea          # Idea Generator only
POST /story/write-story           # Story Writer only
```

### Combined Workflow
```
POST /workflow/generate-full-story    # Complete workflow
POST /workflow/generate-idea-only     # Idea Generator only (workflow endpoint)
GET  /workflow/workflow-info          # System information
```

### Utility Endpoints
```
GET  /idea/idea-examples              # Example prompts
GET  /                               # API overview
GET  /health                         # Health check
```

## Usage Examples

### 1. Complete Workflow (Recommended)
```python
import requests

# Generate both idea and story from a simple prompt
response = requests.post("http://localhost:8000/workflow/generate-full-story", json={
    "prompt": "A mysterious lighthouse keeper",
    "genre": "Mystery",
    "tone": "Dark and atmospheric"
})

result = response.json()
print(f"Title: {result['idea']['title']}")
print(f"Story: {result['story']}")
```

### 2. Idea Generation Only
```python
# Generate just the story idea
response = requests.post("http://localhost:8000/workflow/generate-idea-only", json={
    "prompt": "A time-traveling chef",
    "genre": "Science Fiction"
})

result = response.json()
print(f"Idea: {result['idea']}")
```

### 3. Individual Agents
```python
# Use Idea Generator directly
idea_response = requests.post("http://localhost:8000/idea/generate-idea", json={
    "prompt": "A magical library",
    "genre": "Fantasy"
})

# Use Story Writer with the generated idea
story_response = requests.post("http://localhost:8000/story/write-story", json={
    "title": idea_response.json()["title"],
    "genre": idea_response.json()["genre"],
    "outline": idea_response.json()["outline"]
})
```

## Data Flow

```
User Input (prompt, genre, tone)
    ↓
Idea Generator Agent
    ↓
Story Idea (title, genre, outline, characters, setting)
    ↓
Story Writer Agent
    ↓
Full Story
    ↓
Combined Response (idea + story)
```

## Testing

Run the comprehensive test:
```bash
cd backend
python test/test_full_workflow.py
```

This will test:
- Individual agents
- Idea generation only
- Complete workflow

## Next Steps

The system is ready for the **Editor Agent** implementation, which would:
1. Take the generated story
2. Check for plagiarism
3. Fix grammar and style
4. Format the story
5. Return the final polished story

This would complete the full multi-agent system as shown in the flowchart.
