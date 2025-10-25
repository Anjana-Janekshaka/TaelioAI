#!/usr/bin/env python3
"""
Database initialization script
Creates tables and initial data if they don't exist
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, User, Plan
from db.database import DATABASE_URL

def init_database():
    """Initialize the database with tables and default data"""
    print("Initializing database...")
    
    # Create engine
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
    
    # Create all tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if we need to create default data
        existing_users = db.query(User).count()
        print(f"Found {existing_users} existing users")
        
        # Create default admin user if no users exist
        if existing_users == 0:
            print("Creating default admin user...")
            admin_user = User(
                email="admin@taelio.ai",
                role="admin"
            )
            db.add(admin_user)
            db.flush()
            
            # Create admin plan
            admin_plan = Plan(
                user_id=admin_user.id,
                tier="admin",
                limits_json='{"requests_per_day": 10000, "requests_per_minute": 100, "tokens_per_day": 1000000}'
            )
            db.add(admin_plan)
            
            # Create free tier plan template
            free_plan = Plan(
                user_id="template_free",
                tier="free", 
                limits_json='{"requests_per_day": 50, "requests_per_minute": 2, "tokens_per_day": 10000}'
            )
            db.add(free_plan)
            
            # Create pro tier plan template
            pro_plan = Plan(
                user_id="template_pro",
                tier="pro",
                limits_json='{"requests_per_day": 500, "requests_per_minute": 10, "tokens_per_day": 100000}'
            )
            db.add(pro_plan)
            
            db.commit()
            print("Default data created successfully!")
        else:
            print("Database already has data, skipping default creation")
            
    except Exception as e:
        print(f"Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()
    
    print("Database initialization complete!")

if __name__ == "__main__":
    init_database()
