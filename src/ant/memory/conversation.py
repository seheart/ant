"""Conversation memory management."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from rich.console import Console

console = Console()

# Database location
DB_DIR = Path.home() / ".ant"
DB_FILE = DB_DIR / "conversations.db"


class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(self) -> None:
        self.db_path = DB_FILE
        self.session_id: Optional[str] = None
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize the conversation database."""
        DB_DIR.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
    
    def load_session(self, session_id: str) -> None:
        """Load or create a conversation session."""
        self.session_id = session_id
        
        with sqlite3.connect(self.db_path) as conn:
            # Create session if it doesn't exist
            conn.execute('''
                INSERT OR IGNORE INTO sessions (session_id) VALUES (?)
            ''', (session_id,))
            
            # Update last active time
            conn.execute('''
                UPDATE sessions SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?
            ''', (session_id,))
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a message to the current session."""
        if not self.session_id:
            raise ValueError("No session loaded")
        
        metadata_json = json.dumps(metadata) if metadata else None
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO conversations (session_id, role, content, metadata)
                VALUES (?, ?, ?, ?)
            ''', (self.session_id, role, content, metadata_json))
    
    def get_context_messages(self, limit: int = 20) -> List[Dict[str, str]]:
        """Get recent messages for context."""
        if not self.session_id:
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT role, content FROM conversations 
                WHERE session_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (self.session_id, limit))
            
            messages = [{"role": role, "content": content} for role, content in cursor.fetchall()]
            return list(reversed(messages))  # Reverse to get chronological order
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics for the current session."""
        if not self.session_id:
            return {}
        
        with sqlite3.connect(self.db_path) as conn:
            # Get message count
            cursor = conn.execute('''
                SELECT COUNT(*) FROM conversations WHERE session_id = ?
            ''', (self.session_id,))
            message_count = cursor.fetchone()[0]
            
            # Get session info
            cursor = conn.execute('''
                SELECT created_at, last_active FROM sessions WHERE session_id = ?
            ''', (self.session_id,))
            session_info = cursor.fetchone()
            
            if session_info:
                return {
                    "message_count": message_count,
                    "start_time": session_info[0],
                    "last_active": session_info[1]
                }
        
        return {"message_count": 0}
    
    def clear_session(self) -> None:
        """Clear the current session's conversation history."""
        if not self.session_id:
            return
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                DELETE FROM conversations WHERE session_id = ?
            ''', (self.session_id,))
    
    def save_session(self) -> None:
        """Save session (handled automatically by database)."""
        if self.session_id:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    UPDATE sessions SET last_active = CURRENT_TIMESTAMP WHERE session_id = ?
                ''', (self.session_id,))
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation sessions."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT session_id, created_at, last_active,
                       (SELECT COUNT(*) FROM conversations WHERE session_id = s.session_id) as message_count
                FROM sessions s
                ORDER BY last_active DESC
                LIMIT ?
            ''', (limit,))
            
            return [
                {
                    "session_id": row[0],
                    "created_at": row[1],
                    "last_active": row[2],
                    "message_count": row[3]
                }
                for row in cursor.fetchall()
            ]