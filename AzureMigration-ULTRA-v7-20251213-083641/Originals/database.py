"""
Datenbank - SQLite Integration
"""
import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="kontrollzentrum.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialisiert Datenbank"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("""CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            module TEXT,
            action TEXT,
            status TEXT,
            message TEXT
        )""")
        
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            created_at TEXT
        )""")
        
        conn.commit()
        conn.close()
    
    def log(self, module, action, status, message=""):
        """Schreibt Log-Eintrag"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""INSERT INTO logs (timestamp, module, action, status, message)
                     VALUES (?, ?, ?, ?, ?)""",
                  (datetime.now().isoformat(), module, action, status, message))
        conn.commit()
        conn.close()
    
    def get_logs(self, limit=100):
        """Liest Logs"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        conn.close()
        return rows

db = Database()
