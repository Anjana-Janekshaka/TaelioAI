#!/usr/bin/env python3
"""
Simple web interface to view the database
Run this and go to http://localhost:8080 to view the database
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sqlite3
import json
from datetime import datetime

app = FastAPI()

def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('taelio.db')

@app.get("/", response_class=HTMLResponse)
async def view_database():
    """Display database in a web interface"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TaelioAI Database Viewer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .table { margin: 20px 0; }
            .table h2 { color: #666; border-bottom: 2px solid #eee; padding-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; font-weight: bold; }
            tr:hover { background-color: #f5f5f5; }
            .stats { display: flex; gap: 20px; margin: 20px 0; }
            .stat-card { background: #e3f2fd; padding: 15px; border-radius: 5px; flex: 1; text-align: center; }
            .stat-number { font-size: 24px; font-weight: bold; color: #1976d2; }
            .stat-label { color: #666; margin-top: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗄️ TaelioAI Database Viewer</h1>
    """
    
    try:
        # Get basic stats
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usage")
        usage_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM plans")
        plan_count = cursor.fetchone()[0]
        
        html += f"""
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{user_count}</div>
                    <div class="stat-label">Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{usage_count}</div>
                    <div class="stat-label">Usage Records</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{plan_count}</div>
                    <div class="stat-label">Plans</div>
                </div>
            </div>
        """
        
        # Users table
        cursor.execute("SELECT id, email, role, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        html += """
            <div class="table">
                <h2>👥 Users</h2>
                <table>
                    <tr><th>Email</th><th>Role</th><th>Created</th><th>ID (first 8 chars)</th></tr>
        """
        
        for user in users:
            html += f"""
                <tr>
                    <td>{user[1]}</td>
                    <td>{user[2]}</td>
                    <td>{user[3]}</td>
                    <td>{user[0][:8]}...</td>
                </tr>
            """
        
        html += "</table></div>"
        
        # Plans table
        cursor.execute("SELECT user_id, tier, limits_json, created_at FROM plans ORDER BY created_at DESC")
        plans = cursor.fetchall()
        
        html += """
            <div class="table">
                <h2>📋 Plans</h2>
                <table>
                    <tr><th>User ID</th><th>Tier</th><th>Limits</th><th>Created</th></tr>
        """
        
        for plan in plans:
            try:
                limits = json.loads(plan[2]) if plan[2] else {}
                limits_str = f"Requests: {limits.get('requests_per_day', 'N/A')}/day, {limits.get('requests_per_minute', 'N/A')}/min"
                if 'tokens_per_day' in limits:
                    limits_str += f", Tokens: {limits['tokens_per_day']}/day"
            except:
                limits_str = plan[2] or "No limits"
            
            html += f"""
                <tr>
                    <td>{plan[0][:8]}...</td>
                    <td>{plan[1]}</td>
                    <td>{limits_str}</td>
                    <td>{plan[3]}</td>
                </tr>
            """
        
        html += "</table></div>"
        
        # Usage table (if any)
        if usage_count > 0:
            cursor.execute("SELECT user_id, feature, provider, tokens_in, tokens_out, cost_usd, created_at FROM usage ORDER BY created_at DESC LIMIT 20")
            usage = cursor.fetchall()
            
            html += """
                <div class="table">
                    <h2>📈 Recent Usage</h2>
                    <table>
                        <tr><th>User ID</th><th>Feature</th><th>Provider</th><th>Tokens In</th><th>Tokens Out</th><th>Cost</th><th>Created</th></tr>
            """
            
            for use in usage:
                html += f"""
                    <tr>
                        <td>{use[0][:8]}...</td>
                        <td>{use[1]}</td>
                        <td>{use[2]}</td>
                        <td>{use[3]}</td>
                        <td>{use[4]}</td>
                        <td>${use[5]:.4f}</td>
                        <td>{use[6]}</td>
                    </tr>
                """
            
            html += "</table></div>"
        else:
            html += """
                <div class="table">
                    <h2>📈 Usage</h2>
                    <p>No usage records found. Usage will be tracked when users make API requests.</p>
                </div>
            """
        
    except Exception as e:
        html += f"<p style='color: red;'>Error: {e}</p>"
    finally:
        conn.close()
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html

if __name__ == "__main__":
    import uvicorn
    print("Starting database viewer...")
    print("Open your browser and go to: http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
