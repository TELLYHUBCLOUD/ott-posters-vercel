import sqlite3
import os
from datetime import datetime

DB_PATH = 'ott_posters.db'

def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            image_url TEXT UNIQUE NOT NULL,
            platform TEXT NOT NULL,
            scraped_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def save_to_db(posters):
    """Save posters to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for poster in posters:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO posters (title, image_url, platform, scraped_at)
                VALUES (?, ?, ?, ?)
            ''', (
                poster['title'],
                poster['image_url'],
                poster['platform'],
                poster['scraped_at']
            ))
        except Exception as e:
            print(f"Error saving poster to DB: {e}")
    
    conn.commit()
    conn.close()

def get_recent_posters(platform=None, limit=10):
    """Retrieve recent posters from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = 'SELECT * FROM posters'
    params = []
    
    if platform:
        query += ' WHERE platform = ?'
        params.append(platform)
    
    query += ' ORDER BY scraped_at DESC LIMIT ?'
    params.append(limit)
    
    cursor.execute(query, params)
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return results

# Initialize database on import
init_db()
