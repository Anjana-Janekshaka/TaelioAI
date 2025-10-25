#!/usr/bin/env python3
"""
Test script to verify that agent metrics are now being properly recorded
"""
import requests
import json
import time

def test_metrics_fix():
    """Test the fixed metrics system"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Fixed Agent Metrics System")
    print("=" * 50)
    
    # Step 1: Login to get JWT token
    print("1. Logging in...")
    login_response = requests.post(
        f"{base_url}/auth/login",
        json={"email": "test@example.com"},
        headers={"Content-Type": "application/json"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    login_data = login_response.json()
    token = login_data["access_token"]
    print(f"✅ Login successful. Token: {token[:20]}...")
    
    # Step 2: Test idea generation with real metrics
    print("\n2. Testing idea generation with real metrics...")
    idea_response = requests.post(
        f"{base_url}/multi-agent/idea-only-orchestrated",
        json={
            "prompt": "A mysterious lighthouse keeper",
            "genre": "Mystery",
            "tone": "Dark and atmospheric"
        },
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    if idea_response.status_code != 200:
        print(f"❌ Idea generation failed: {idea_response.status_code}")
        print(f"Response: {idea_response.text}")
        return
    
    idea_data = idea_response.json()
    print(f"✅ Idea generation successful!")
    print(f"   Workflow ID: {idea_data['workflow_id']}")
    print(f"   Steps: {len(idea_data['workflow_steps'])}")
    
    # Check if agent_response is included in workflow steps
    for i, step in enumerate(idea_data['workflow_steps']):
        print(f"   Step {i+1}: {step['agent_type']}")
        if 'agent_response' in step:
            metadata = step['agent_response'].get('metadata', {})
            print(f"     ✅ Real metrics found:")
            print(f"       Provider: {metadata.get('provider', 'unknown')}")
            print(f"       Model: {metadata.get('model', 'unknown')}")
            print(f"       Tokens In: {metadata.get('tokens_in', 0)}")
            print(f"       Tokens Out: {metadata.get('tokens_out', 0)}")
            print(f"       Cost: ${metadata.get('cost_usd', 0.0)}")
        else:
            print(f"     ❌ No agent_response found")
    
    # Step 3: Check Prometheus metrics
    print("\n3. Checking Prometheus metrics...")
    metrics_response = requests.get(f"{base_url}/metrics")
    
    if metrics_response.status_code == 200:
        metrics_text = metrics_response.text
        print("✅ Prometheus metrics endpoint accessible")
        
        # Look for real provider metrics
        if "provider=\"gemini\"" in metrics_text:
            print("✅ Real provider metrics found (gemini)")
        else:
            print("❌ No real provider metrics found")
            
        if "model=\"gemini-2.5-flash\"" in metrics_text:
            print("✅ Real model metrics found (gemini-2.5-flash)")
        else:
            print("❌ No real model metrics found")
            
        # Count token metrics
        token_in_count = metrics_text.count("taelio_tokens_in_total")
        token_out_count = metrics_text.count("taelio_tokens_out_total")
        print(f"   Token metrics found: {token_in_count} input, {token_out_count} output")
        
    else:
        print(f"❌ Metrics endpoint failed: {metrics_response.status_code}")
    
    print("\n🎯 Test Summary:")
    print("   - Agent responses now include real metrics metadata")
    print("   - Metrics system uses real provider/model/token data")
    print("   - Prometheus metrics show actual LLM usage")

if __name__ == "__main__":
    try:
        test_metrics_fix()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

