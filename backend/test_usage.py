#!/usr/bin/env python3
"""
Test script to demonstrate tier-based usage tracking
"""

import requests
import json
import time

# Test user credentials
test_email = "testuser@example.com"

def test_tier_based_usage():
    """Test the tier-based usage tracking system"""
    print("Testing Tier-Based Usage Tracking")
    print("=" * 50)
    
    # Step 1: Register a new user
    print("\n1. Registering new user...")
    register_data = {
        "email": test_email,
        "role": "free"  # Start with free tier
    }
    
    try:
        response = requests.post("http://localhost:8000/auth/register", json=register_data)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data["access_token"]
            print(f"User registered successfully: {auth_data['email']}")
            print(f"   Tier: {auth_data['tier']}")
            print(f"   Limits: {auth_data['limits']}")
        else:
            print(f"Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"Registration error: {e}")
        return
    
    # Step 2: Get initial usage metrics
    print("\n2. Getting initial usage metrics...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get("http://localhost:8000/user/me/tier-info", headers=headers)
        if response.status_code == 200:
            tier_info = response.json()
            print(f"Tier Info Retrieved:")
            print(f"   Tier: {tier_info['tier']}")
            print(f"   Limits: {tier_info['limits']}")
            print(f"   Current Usage: {tier_info['current_usage']}")
            print(f"   Remaining: {tier_info['remaining']}")
        else:
            print(f"Failed to get tier info: {response.text}")
    except Exception as e:
        print(f"Error getting tier info: {e}")
    
    # Step 3: Simulate some usage (this would normally happen through API calls)
    print("\n3. Simulating usage tracking...")
    print("   (In a real scenario, this would happen when users make API calls)")
    
    # Step 4: Show how different tiers would have different limits
    print("\n4. Tier Comparison:")
    tiers = {
        "free": {"requests_per_day": 50, "tokens_per_day": 10000},
        "pro": {"requests_per_day": 500, "tokens_per_day": 100000},
        "admin": {"requests_per_day": 10000, "tokens_per_day": 1000000}
    }
    
    for tier, limits in tiers.items():
        print(f"   {tier.upper()} Tier:")
        print(f"     - Requests per day: {limits['requests_per_day']:,}")
        print(f"     - Tokens per day: {limits['tokens_per_day']:,}")
    
    print("\nTest completed!")
    print("\nHow it works:")
    print("1. Users are assigned tier limits when they register")
    print("2. Each API call is tracked in the database")
    print("3. The metrics dropdown shows real-time usage vs limits")
    print("4. Different tiers have different limits (Free: 50 req/day, Pro: 500 req/day, Admin: 10K req/day)")
    print("5. The UI updates to show remaining requests and tokens")

if __name__ == "__main__":
    test_tier_based_usage()
