import sqlite3
import os
from werkzeug.security import generate_password_hash

from config import Config
DB_NAME = Config.DATABASE

def connect():
    os.makedirs("instance", exist_ok=True)
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # VIOLATIONS TABLE (if not already)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS violations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image TEXT,
        result TEXT,
        confidence REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def get_all_detections():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT image_path, result, confidence, timestamp
        FROM detections
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def create_admin():
    conn = connect()
    cur = conn.cursor()

    username = "admin"
    password = generate_password_hash("admin123")

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except:
        pass 

    conn.close()

    