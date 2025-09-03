import requests
import json

# API endpoint
url = "http://localhost:8000/story/write-story"

# Sample data for the POST request
data = {
    "title": "The Mysterious Forest",
    "genre": "Fantasy",
    "outline": "A young explorer discovers a magical forest where trees can talk and animals have special powers. They must solve a mystery to save the forest from an ancient curse."
}

# Make the POST request
try:
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Success! Story generated:")
        print(f"Title: {data['title']}")
        print(f"Genre: {data['genre']}")
        print(f"Outline: {data['outline']}")
        print("\n" + "="*50)
        print("Generated Story:")
        print("="*50)
        print(result['story'])
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Connection error: Make sure the backend is running on http://localhost:8000")
except Exception as e:
    print(f"❌ Error: {e}")
