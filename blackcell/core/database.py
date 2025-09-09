"""
BlackCell Security Toolkit - Database Interface
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from blackcell.core.logger import setup_logger

class Database:
    """Simple SQLite database for storing results and configuration"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_dir = Path.home() / ".blackcell" / "data"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / "blackcell.db")
        
        self.db_path = db_path
        self.logger = setup_logger("database")
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Scan results table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scan_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target TEXT NOT NULL,
                        scan_type TEXT NOT NULL,
                        results TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Payloads table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS payloads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT NOT NULL,
                        payload TEXT NOT NULL,
                        description TEXT,
                        tags TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                self.logger.info(f"Database initialized: {self.db_path}")
                
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
    
    def save_scan_result(self, target: str, scan_type: str, results: Dict[str, Any]) -> int:
        """Save scan results to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO scan_results (target, scan_type, results) VALUES (?, ?, ?)",
                    (target, scan_type, json.dumps(results))
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            self.logger.error(f"Failed to save scan result: {e}")
            return -1
    
    def get_scan_results(self, target: Optional[str] = None, 
                        scan_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get scan results from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM scan_results"
                params = []
                
                if target or scan_type:
                    conditions = []
                    if target:
                        conditions.append("target = ?")
                        params.append(target)
                    if scan_type:
                        conditions.append("scan_type = ?")
                        params.append(scan_type)
                    query += " WHERE " + " AND ".join(conditions)
                
                query += " ORDER BY timestamp DESC"
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                results = []
                for row in rows:
                    results.append({
                        "id": row[0],
                        "target": row[1],
                        "scan_type": row[2],
                        "results": json.loads(row[3]),
                        "timestamp": row[4]
                    })
                
                return results
                
        except Exception as e:
            self.logger.error(f"Failed to get scan results: {e}")
            return []