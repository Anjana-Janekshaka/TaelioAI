#!/usr/bin/env python3
"""
Simple rate limiting test that doesn't require story generation
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "ratelimit_simple@example.com"

def test_simple_rate_limiting():
    """Test rate limiting with simple API calls"""
    print("Testing Simple Rate Limiting System")
    print("=" * 50)
    
    # Step 1: Register a test user
    print("\n1. Registering test user...")
    register_data = {
        "email": TEST_EMAIL,
        "role": "free"  # Start with free tier (50 requests/day, 2 requests/minute)
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
            print(f"  - Limits: {limits}")
        else:
            print(f"Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"Registration error: {e}")
        return
    
    # Step 2: Test rate limiting with rapid API calls
    print(f"\n2. Testing rate limiting with rapid API calls...")
    print(f"   Free tier limits: {limits['requests_per_day']} requests/day, {limits['requests_per_minute']} requests/minute")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test multiple rapid requests to trigger rate limiting
    for i in range(10):  # Try 10 requests rapidly
        print(f"\n   Request {i+1}/10:")
        
        try:
            start_time = time.time()
            # Use a simple endpoint that doesn't require AI generation
            response = requests.get(f"{BASE_URL}/user/me/profile", headers=headers)
            end_time = time.time()
            
            if response.status_code == 200:
                print(f"     Success (took {end_time - start_time:.2f}s)")
            elif response.status_code == 429:
                rate_limit_data = response.json()
                print(f"     Rate limit exceeded!")
                print(f"     Details: {rate_limit_data.get('detail', {}).get('message', 'Unknown error')}")
                print(f"     Remaining: {rate_limit_data.get('detail', {}).get('remaining', {})}")
                break
            else:
                print(f"     Error {response.status_code}: {response.text}")
                break
                
        except Exception as e:
            print(f"     Request failed: {e}")
            break
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Step 3: Check usage metrics
    print(f"\n3. Checking usage metrics...")
    try:
        response = requests.get(f"{BASE_URL}/user/me/usage?days=1", headers=headers)
        if response.status_code == 200:
            usage_data = response.json()
            print(f"Usage Summary:")
            print(f"  - Total requests: {usage_data['total_requests']}")
            print(f"  - Total tokens: {usage_data['total_tokens_in'] + usage_data['total_tokens_out']}")
            print(f"  - Total cost: ${usage_data['total_cost']:.4f}")
        else:
            print(f"Failed to get usage data: {response.text}")
    except Exception as e:
        print(f"Error getting usage data: {e}")
    
    # Step 4: Check tier info with remaining limits
    print(f"\n4. Checking tier information...")
    try:
        response = requests.get(f"{BASE_URL}/user/me/tier-info", headers=headers)
        if response.status_code == 200:
            tier_info = response.json()
            print(f"Tier Information:")
            print(f"  - Tier: {tier_info['tier']}")
            print(f"  - Limits: {tier_info['limits']}")
            print(f"  - Current Usage: {tier_info['current_usage']}")
            print(f"  - Remaining: {tier_info['remaining']}")
        else:
            print(f"Failed to get tier info: {response.text}")
    except Exception as e:
        print(f"Error getting tier info: {e}")
    
    print(f"\nRate limiting test completed!")
    print(f"\nRate Limiting Features:")
    print(f"1. Database-backed usage tracking")
    print(f"2. Tier-based rate limits (Free: 50/day, Pro: 500/day, Admin: 10K/day)")
    print(f"3. Per-minute rate limiting (Free: 2/min, Pro: 10/min, Admin: 100/min)")
    print(f"4. Token-based limits (Free: 10K/day, Pro: 100K/day, Admin: 1M/day)")
    print(f"5. Real-time remaining limits calculation")
    print(f"6. Rate limit headers in responses")
    print(f"7. Graceful error handling with retry information")

if __name__ == "__main__":
    test_simple_rate_limiting()
