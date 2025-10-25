#!/usr/bin/env python3
"""
Database viewer script
Shows all tables and data in the TaelioAI database
"""

import sqlite3
import json
from datetime import datetime

def view_database():
    """View all data in the database"""
    print("TaelioAI Database Viewer")
    print("=" * 50)
    
    # Connect to database
    conn = sqlite3.connect('taelio.db')
    cursor = conn.cursor()
    
    try:
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\nFound {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        print("\n" + "=" * 50)
        
        # View each table
        for table_name in [table[0] for table in tables]:
            print(f"\nTable: {table_name.upper()}")
            print("-" * 30)
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            if columns:
                print("Columns:")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"\nTotal rows: {count}")
            
            if count > 0:
                # Get all data
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
                rows = cursor.fetchall()
                
                print(f"\nFirst {min(10, count)} rows:")
                for i, row in enumerate(rows, 1):
                    print(f"  Row {i}: {row}")
                
                if count > 10:
                    print(f"  ... and {count - 10} more rows")
            
            print()
        
        # Show specific user data
        print("USER DATA SUMMARY")
        print("-" * 30)
        
        # Users
        cursor.execute("SELECT id, email, role, created_at FROM users;")
        users = cursor.fetchall()
        print(f"\nUsers ({len(users)}):")
        for user in users:
            print(f"  - {user[1]} ({user[2]}) - ID: {user[0][:8]}... - Created: {user[3]}")
        
        # Plans
        cursor.execute("SELECT user_id, tier, limits_json FROM plans;")
        plans = cursor.fetchall()
        print(f"\nPlans ({len(plans)}):")
        for plan in plans:
            limits = json.loads(plan[2]) if plan[2] else {}
            print(f"  - User: {plan[0][:8]}... - Tier: {plan[1]} - Limits: {limits}")
        
        # Usage
        cursor.execute("SELECT COUNT(*) FROM usage;")
        usage_count = cursor.fetchone()[0]
        print(f"\nUsage Records: {usage_count}")
        
        if usage_count > 0:
            cursor.execute("SELECT user_id, feature, provider, tokens_in, tokens_out, cost_usd, created_at FROM usage ORDER BY created_at DESC LIMIT 5;")
            recent_usage = cursor.fetchall()
            print("Recent usage:")
            for usage in recent_usage:
                print(f"  - {usage[1]} via {usage[2]} - {usage[3]}/{usage[4]} tokens - ${usage[5]:.4f} - {usage[6]}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    
    print("\nDatabase view complete!")

if __name__ == "__main__":
    view_database()
