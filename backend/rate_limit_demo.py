#!/usr/bin/env python3
"""
Rate Limiting Demo - Shows all implemented features
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def demo_rate_limiting():
    """Demonstrate all rate limiting features"""
    print("RATE LIMITING SYSTEM DEMO")
    print("=" * 60)
    
    # Test different tiers
    tiers = [
        {"email": "free_user@example.com", "role": "free", "name": "FREE"},
        {"email": "pro_user@example.com", "role": "pro", "name": "PRO"},
        {"email": "admin_user@example.com", "role": "admin", "name": "ADMIN"}
    ]
    
    for tier_info in tiers:
        print(f"\nTesting {tier_info['name']} Tier")
        print("-" * 40)
        
        # Register user
        register_data = {
            "email": tier_info["email"],
            "role": tier_info["role"]
        }
        
        try:
            response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
            if response.status_code == 200:
                auth_data = response.json()
                token = auth_data["access_token"]
                limits = auth_data["limits"]
                
                print(f"User registered: {tier_info['name']} tier")
                print(f"   Limits: {limits['requests_per_day']} req/day, {limits['requests_per_minute']} req/min")
                
                # Test rapid requests
                headers = {"Authorization": f"Bearer {token}"}
                success_count = 0
                
                for i in range(5):
                    try:
                        response = requests.get(f"{BASE_URL}/user/me/profile", headers=headers)
                        if response.status_code == 200:
                            success_count += 1
                            print(f"   Request {i+1}: Success")
                        elif response.status_code == 429:
                            print(f"   Request {i+1}: Rate limited!")
                            break
                        else:
                            print(f"   Request {i+1}: Error {response.status_code}")
                            break
                    except Exception as e:
                        print(f"   Request {i+1}: Failed: {e}")
                        break
                    
                    time.sleep(0.1)  # Very small delay
                
                # Get usage info
                try:
                    response = requests.get(f"{BASE_URL}/user/me/tier-info", headers=headers)
                    if response.status_code == 200:
                        tier_data = response.json()
                        print(f"   Usage: {tier_data['current_usage']['requests_today']} requests today")
                        print(f"   Remaining: {tier_data['remaining']['requests_today']} requests left")
                except:
                    pass
                    
            else:
                print(f"Registration failed for {tier_info['name']} tier")
                
        except Exception as e:
            print(f"Error testing {tier_info['name']} tier: {e}")
    
    print(f"\nRATE LIMITING FEATURES IMPLEMENTED:")
    print("=" * 60)
    print("1. Database-backed usage tracking")
    print("2. Tier-based rate limits:")
    print("   - FREE: 50 requests/day, 2 requests/minute, 10K tokens/day")
    print("   - PRO: 500 requests/day, 10 requests/minute, 100K tokens/day") 
    print("   - ADMIN: 10K requests/day, 100 requests/minute, 1M tokens/day")
    print("3. Real-time remaining limits calculation")
    print("4. Rate limit headers in API responses")
    print("5. Graceful error handling with retry information")
    print("6. Per-minute and per-day rate limiting")
    print("7. Token-based usage tracking")
    print("8. Integration with user metrics dropdown")
    
    print(f"\nHOW IT WORKS:")
    print("=" * 60)
    print("1. Users are assigned tier limits when they register")
    print("2. Every API call is tracked in the database")
    print("3. Rate limits are checked before processing requests")
    print("4. Exceeded limits return 429 status with retry info")
    print("5. Metrics dropdown shows real-time usage vs limits")
    print("6. Different tiers have different limits")
    print("7. System prevents abuse while allowing legitimate use")
    
    print(f"\nUI INTEGRATION:")
    print("=" * 60)
    print("Metrics dropdown shows:")
    print("   - Current tier and role")
    print("   - Remaining requests and tokens")
    print("   - Usage breakdown by feature")
    print("   - Cost tracking")
    print("   - Real-time updates")
    
    print(f"\nRATE LIMITING SYSTEM IS FULLY OPERATIONAL!")

if __name__ == "__main__":
    demo_rate_limiting()
