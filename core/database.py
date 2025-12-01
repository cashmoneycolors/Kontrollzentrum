"""Database Layer - Persistierung aller Daten"""
import sqlite3
import json
from datetime import datetime
from typing import Any, Dict, List

class Database:
    def __init__(self, db_path: str = "kontrollzentrum.db"):
        self.db_path = db_path
        self.init_schema()
    
    def init_schema(self):
        """Initialize all tables"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Module results
        c.execute("""CREATE TABLE IF NOT EXISTS module_results (
            id INTEGER PRIMARY KEY,
            module_name TEXT,
            execution_time REAL,
            result TEXT,
            status TEXT,
            timestamp TEXT
        )""")
        
        # Configuration
        c.execute("""CREATE TABLE IF NOT EXISTS config (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT
        )""")
        
        # Audit log
        c.execute("""CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY,
            action TEXT,
            user TEXT,
            details TEXT,
            timestamp TEXT
        )""")
        
        conn.commit()
        conn.close()
    
    def save_result(self, module_name: str, result: Dict, status: str, exec_time: float):
        """Save module execution result"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""INSERT INTO module_results 
                     VALUES (NULL, ?, ?, ?, ?, ?)""",
                  (module_name, exec_time, json.dumps(result), status, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_results(self, module_name: str = None, limit: int = 100) -> List[Dict]:
        """Get module results"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        if module_name:
            c.execute("""SELECT * FROM module_results 
                        WHERE module_name = ? 
                        ORDER BY id DESC LIMIT ?""", (module_name, limit))
        else:
            c.execute("""SELECT * FROM module_results 
                        ORDER BY id DESC LIMIT ?""", (limit,))
        
        results = [{"id": row[0], "module": row[1], "exec_time": row[2], 
                   "result": json.loads(row[3]), "status": row[4], "timestamp": row[5]} 
                   for row in c.fetchall()]
        conn.close()
        return results
    
    def set_config(self, key: str, value: Any):
        """Store configuration"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""INSERT OR REPLACE INTO config VALUES (?, ?, ?)""",
                  (key, json.dumps(value), datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_config(self, key: str) -> Any:
        """Get configuration"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = c.fetchone()
        conn.close()
        return json.loads(row[0]) if row else None
    
    def audit(self, action: str, user: str, details: str):
        """Log audit event"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""INSERT INTO audit_log VALUES (NULL, ?, ?, ?, ?)""",
                  (action, user, details, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        """Get audit log"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT ?", (limit,))
        logs = [{"id": row[0], "action": row[1], "user": row[2], "details": row[3], "timestamp": row[4]} 
                for row in c.fetchall()]
        conn.close()
        return logs

db = Database()
