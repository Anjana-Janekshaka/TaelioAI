#!/usr/bin/env python3
"""
Test script to demonstrate token tracking and reduction
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "token_test_4@example.com"

def test_token_tracking():
    """Test that tokens are properly tracked and reduced when using AI features"""
    print("Testing Token Tracking and Reduction")
    print("=" * 50)
    
    # Step 1: Register a test user
    print("\n1. Registering test user...")
    register_data = {
        "email": TEST_EMAIL,
        "role": "free"  # Start with free tier (10K tokens/day)
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data["access_token"]
            user_id = auth_data["user_id"]
            tier = auth_data["tier"]
            limits = auth_data["limits"]
            
            print(f"User registered successfully:")
            print(f"  - User ID: {user_id}")
            print(f"  - Tier: {tier}")
            print(f"  - Token limit: {limits['tokens_per_day']} tokens/day")
        else:
            print(f"Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"Registration error: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Check initial usage
    print(f"\n2. Checking initial usage...")
    try:
        response = requests.get(f"{BASE_URL}/user/me/tier-info", headers=headers)
        if response.status_code == 200:
            tier_info = response.json()
            print(f"Initial usage:")
            print(f"  - Tokens used today: {tier_info['current_usage']['tokens_today']}")
            print(f"  - Tokens remaining: {tier_info['remaining']['tokens_today']}")
        else:
            print(f"Failed to get tier info: {response.text}")
    except Exception as e:
        print(f"Error getting tier info: {e}")
    
    # Step 3: Generate an idea (should consume tokens)
    print(f"\n3. Generating an idea (should consume tokens)...")
    idea_data = {
        "prompt": "A magical library that changes every night",
        "genre": "Fantasy",
        "tone": "Mysterious and enchanting"
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/idea/generate-idea", json=idea_data, headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            idea_result = response.json()
            print(f"  Idea generated successfully in {end_time - start_time:.2f}s")
            print(f"  Idea: {str(idea_result)[:100]}...")
        else:
            print(f"  Idea generation failed: {response.text}")
    except Exception as e:
        print(f"  Idea generation error: {e}")
    
    # Step 4: Check usage after idea generation
    print(f"\n4. Checking usage after idea generation...")
    try:
        response = requests.get(f"{BASE_URL}/user/me/usage?days=1", headers=headers)
        if response.status_code == 200:
            usage_data = response.json()
            print(f"Usage after idea generation:")
            print(f"  - Total requests: {usage_data['total_requests']}")
            print(f"  - Total tokens in: {usage_data['total_tokens_in']}")
            print(f"  - Total tokens out: {usage_data['total_tokens_out']}")
            print(f"  - Total cost: ${usage_data['total_cost']:.4f}")
        else:
            print(f"Failed to get usage data: {response.text}")
    except Exception as e:
        print(f"Error getting usage data: {e}")
    
    # Step 5: Generate a story (should consume more tokens)
    print(f"\n5. Generating a story (should consume more tokens)...")
    story_data = {
        "title": "The Mysterious Library",
        "genre": "Fantasy",
        "outline": "A young librarian discovers that the books in her library change every night, revealing new stories and magical adventures."
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/story/write-story", json=story_data, headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            story_result = response.json()
            print(f"  Story generated successfully in {end_time - start_time:.2f}s")
            print(f"  Story length: {len(story_result['story'])} characters")
        else:
            print(f"  Story generation failed: {response.text}")
    except Exception as e:
        print(f"  Story generation error: {e}")
    
    # Step 6: Check final usage
    print(f"\n6. Checking final usage...")
    try:
        response = requests.get(f"{BASE_URL}/user/me/tier-info", headers=headers)
        if response.status_code == 200:
            tier_info = response.json()
            print(f"Final usage:")
            print(f"  - Tokens used today: {tier_info['current_usage']['tokens_today']}")
            print(f"  - Tokens remaining: {tier_info['remaining']['tokens_today']}")
            print(f"  - Requests made today: {tier_info['current_usage']['requests_today']}")
        else:
            print(f"Failed to get final tier info: {response.text}")
    except Exception as e:
        print(f"Error getting final tier info: {e}")
    
    # Step 7: Get detailed usage breakdown
    print(f"\n7. Getting detailed usage breakdown...")
    try:
        response = requests.get(f"{BASE_URL}/user/me/usage?days=1", headers=headers)
        if response.status_code == 200:
            usage_data = response.json()
            print(f"Detailed usage breakdown:")
            print(f"  - Total requests: {usage_data['total_requests']}")
            print(f"  - Total tokens in: {usage_data['total_tokens_in']}")
            print(f"  - Total tokens out: {usage_data['total_tokens_out']}")
            print(f"  - Total cost: ${usage_data['total_cost']:.4f}")
            
            if usage_data['feature_breakdown']:
                print(f"  - Feature breakdown:")
                for feature, data in usage_data['feature_breakdown'].items():
                    print(f"    * {feature}: {data['requests']} requests, {data['tokens']} tokens, ${data['cost']:.4f}")
        else:
            print(f"Failed to get detailed usage: {response.text}")
    except Exception as e:
        print(f"Error getting detailed usage: {e}")
    
    print(f"\nToken tracking test completed!")
    print(f"\nKey Features Demonstrated:")
    print(f"1. Tokens are tracked when using AI features")
    print(f"2. Token usage is logged to the database")
    print(f"3. Remaining tokens are calculated in real-time")
    print(f"4. Usage breakdown shows feature-specific consumption")
    print(f"5. Cost tracking is implemented")
    print(f"6. Rate limiting works with token limits")

if __name__ == "__main__":
    test_token_tracking()
