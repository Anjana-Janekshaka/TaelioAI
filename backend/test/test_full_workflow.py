import requests
import json

# Test the full multi-agent workflow
def test_full_workflow():
    """Test the complete Idea Generator + Story Writer workflow"""
    
    # API endpoint for full workflow
    url = "http://localhost:8000/workflow/generate-full-story"
    
    # Test data
    data = {
        "prompt": "A mysterious lighthouse keeper who discovers something strange",
        "genre": "Mystery",
        "tone": "Dark and atmospheric"
    }
    
    print("🚀 Testing Full Multi-Agent Workflow")
    print("=" * 50)
    print(f"Input Prompt: {data['prompt']}")
    print(f"Genre: {data['genre']}")
    print(f"Tone: {data['tone']}")
    print("\n" + "=" * 50)
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ SUCCESS! Full workflow completed")
            print("\n" + "=" * 30 + " GENERATED IDEA " + "=" * 30)
            print(f"Title: {result['idea']['title']}")
            print(f"Genre: {result['idea']['genre']}")
            print(f"Characters: {result['idea']['characters']}")
            print(f"Setting: {result['idea']['setting']}")
            print(f"Outline: {result['idea']['outline']}")
            
            print("\n" + "=" * 30 + " GENERATED STORY " + "=" * 30)
            print(result['story'])
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_idea_only():
    """Test just the Idea Generator agent"""
    
    url = "http://localhost:8000/workflow/generate-idea-only"
    
    data = {
        "prompt": "A time-traveling chef",
        "genre": "Science Fiction",
        "tone": "Light-hearted"
    }
    
    print("\n🧠 Testing Idea Generator Only")
    print("=" * 50)
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Idea generated")
            print(f"Title: {result['idea']['title']}")
            print(f"Genre: {result['idea']['genre']}")
            print(f"Outline: {result['idea']['outline']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_individual_agents():
    """Test individual agents separately"""
    
    print("\n🔧 Testing Individual Agents")
    print("=" * 50)
    
    # Test Idea Generator
    idea_url = "http://localhost:8000/idea/generate-idea"
    idea_data = {
        "prompt": "A magical library",
        "genre": "Fantasy"
    }
    
    try:
        response = requests.post(idea_url, json=idea_data)
        if response.status_code == 200:
            print("✅ Idea Generator: Working")
        else:
            print(f"❌ Idea Generator: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Idea Generator: {e}")
    
    # Test Story Writer (using existing endpoint)
    story_url = "http://localhost:8000/story/write-story"
    story_data = {
        "title": "The Enchanted Library",
        "genre": "Fantasy",
        "outline": "A librarian discovers a magical section of the library where books come to life."
    }
    
    try:
        response = requests.post(story_url, json=story_data)
        if response.status_code == 200:
            print("✅ Story Writer: Working")
        else:
            print(f"❌ Story Writer: Error {response.status_code}")
    except Exception as e:
        print(f"❌ Story Writer: {e}")

if __name__ == "__main__":
    print("TaelioAI Multi-Agent System Test")
    print("=" * 50)
    
    # Test individual agents first
    test_individual_agents()
    
    # Test idea generation only
    test_idea_only()
    
    # Test full workflow
    test_full_workflow()
