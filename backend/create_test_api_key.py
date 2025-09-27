#!/usr/bin/env python3
"""
Script to create a test API key for development
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth.api_keys import create_api_key, generate_api_key
from db.database import get_db
from db.models import User, ApiKey
from sqlalchemy.orm import Session

def create_test_user_and_api_key():
    """Create a test user and API key for development"""
    
    # Get database session
    db = next(get_db())
    
    try:
        # Create test user if not exists
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            test_user = User(
                id="test-user-123",
                email="test@example.com",
                role="pro",
                hashed_password="dummy_hash"  # For development only
            )
            db.add(test_user)
            db.commit()
            print("✅ Created test user: test@example.com")
        else:
            print("✅ Test user already exists: test@example.com")
        
        # Create API key
        api_key = create_api_key(
            user_id=test_user.id,
            name="Development Test Key",
            db=db
        )
        
        print(f"✅ Created API key: {api_key}")
        print(f"📋 User ID: {test_user.id}")
        print(f"📋 User Email: {test_user.email}")
        print(f"📋 User Role: {test_user.role}")
        
        return api_key
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("🔑 Creating test API key...")
    api_key = create_test_user_and_api_key()
    
    if api_key:
        print("\n🎯 How to use this API key:")
        print(f"curl -X POST http://localhost:8000/idea/generate-idea \\")
        print(f"  -H 'X-API-Key: {api_key}' \\")
        print(f"  -H 'Content-Type: application/json' \\")
        print(f"  -d '{{\"prompt\": \"A mysterious lighthouse keeper\"}}'")
    else:
        print("❌ Failed to create API key")
