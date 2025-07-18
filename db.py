import sqlite3

def init_db():
    conn = sqlite3.connect("f1_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            location TEXT,
            latitude REAL,
            longitude REAL,
            category TEXT,
            language TEXT,
            title TEXT,
            content TEXT,
            audio_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_submission(name, location, category, language, title, content, audio_path=None, email=None, lat=None, lon=None):
    conn = sqlite3.connect("f1_data.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO submissions 
        (name, email, location, latitude, longitude, category, language, title, content, audio_path) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, email, location, lat, lon, category, language, title, content, audio_path))
    conn.commit()
    conn.close()
