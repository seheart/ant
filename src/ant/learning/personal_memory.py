"""Personal memory system for learning about Seth as a person."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from ant.cli.setup import get_config


class PersonalMemory:
    """Stores and retrieves personal information about Seth."""
    
    def __init__(self):
        self.config = get_config()
        self.db_path = Path(self.config["data_dir"]) / "personal_memory.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize the personal memory database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS personality_traits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    trait_name TEXT NOT NULL,
                    trait_value TEXT NOT NULL,
                    confidence REAL DEFAULT 0.5,
                    first_observed TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    notes TEXT,
                    UNIQUE(category, trait_name)
                );
                
                CREATE TABLE IF NOT EXISTS conversation_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_date TEXT NOT NULL,
                    insight_type TEXT NOT NULL,
                    insight TEXT NOT NULL,
                    context TEXT,
                    confidence REAL DEFAULT 0.5,
                    timestamp TEXT NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS personal_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    preference_name TEXT NOT NULL,
                    preference_value TEXT NOT NULL,
                    reasoning TEXT,
                    confidence REAL DEFAULT 0.5,
                    first_noted TEXT NOT NULL,
                    last_confirmed TEXT NOT NULL,
                    UNIQUE(category, preference_name)
                );
                
                CREATE TABLE IF NOT EXISTS relationship_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context_type TEXT NOT NULL,
                    context_key TEXT NOT NULL,
                    context_value TEXT NOT NULL,
                    importance REAL DEFAULT 0.5,
                    last_updated TEXT NOT NULL,
                    UNIQUE(context_type, context_key)
                );
                
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    conversation_topic TEXT,
                    key_insights TEXT,
                    seth_mood TEXT,
                    conversation_quality TEXT,
                    learned_something_new BOOLEAN DEFAULT FALSE
                );
            """)
    
    def record_personality_trait(self, category: str, trait_name: str, 
                                trait_value: str, confidence: float = 0.5, 
                                notes: str = None):
        """Record a personality trait about Seth."""
        with sqlite3.connect(self.db_path) as conn:
            now = datetime.now().isoformat()
            conn.execute("""
                INSERT OR REPLACE INTO personality_traits 
                (category, trait_name, trait_value, confidence, first_observed, last_updated, notes)
                VALUES (?, ?, ?, ?, 
                    COALESCE((SELECT first_observed FROM personality_traits 
                             WHERE category = ? AND trait_name = ?), ?),
                    ?, ?)
            """, (category, trait_name, trait_value, confidence, 
                  category, trait_name, now, now, notes))
    
    def record_conversation_insight(self, insight_type: str, insight: str, 
                                   context: str = None, confidence: float = 0.5):
        """Record an insight from our conversation."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO conversation_insights 
                (session_date, insight_type, insight, context, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (datetime.now().date().isoformat(), insight_type, insight, 
                  context, confidence, datetime.now().isoformat()))
    
    def record_personal_preference(self, category: str, preference_name: str,
                                  preference_value: str, reasoning: str = None,
                                  confidence: float = 0.5):
        """Record a personal preference."""
        with sqlite3.connect(self.db_path) as conn:
            now = datetime.now().isoformat()
            conn.execute("""
                INSERT OR REPLACE INTO personal_preferences
                (category, preference_name, preference_value, reasoning, confidence, 
                 first_noted, last_confirmed)
                VALUES (?, ?, ?, ?, ?,
                    COALESCE((SELECT first_noted FROM personal_preferences 
                             WHERE category = ? AND preference_name = ?), ?),
                    ?)
            """, (category, preference_name, preference_value, reasoning, confidence,
                  category, preference_name, now, now))
    
    def update_relationship_context(self, context_type: str, context_key: str,
                                   context_value: str, importance: float = 0.5):
        """Update relationship context (how we communicate, what matters to Seth, etc.)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO relationship_context
                (context_type, context_key, context_value, importance, last_updated)
                VALUES (?, ?, ?, ?, ?)
            """, (context_type, context_key, context_value, importance, 
                  datetime.now().isoformat()))
    
    def log_conversation_session(self, session_id: str, topic: str = None,
                                key_insights: str = None, seth_mood: str = None,
                                conversation_quality: str = None, 
                                learned_something_new: bool = False):
        """Log overall conversation session information."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO conversation_history
                (session_id, timestamp, conversation_topic, key_insights, 
                 seth_mood, conversation_quality, learned_something_new)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (session_id, datetime.now().isoformat(), topic, key_insights,
                  seth_mood, conversation_quality, learned_something_new))
    
    def get_personality_profile(self) -> Dict[str, Any]:
        """Get Seth's personality profile."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Get personality traits
            traits = {}
            for row in conn.execute("""
                SELECT category, trait_name, trait_value, confidence, notes
                FROM personality_traits 
                ORDER BY confidence DESC, last_updated DESC
            """):
                if row['category'] not in traits:
                    traits[row['category']] = {}
                traits[row['category']][row['trait_name']] = {
                    'value': row['trait_value'],
                    'confidence': row['confidence'],
                    'notes': row['notes']
                }
            
            # Get preferences
            preferences = {}
            for row in conn.execute("""
                SELECT category, preference_name, preference_value, reasoning, confidence
                FROM personal_preferences
                ORDER BY confidence DESC, last_confirmed DESC
            """):
                if row['category'] not in preferences:
                    preferences[row['category']] = {}
                preferences[row['category']][row['preference_name']] = {
                    'value': row['preference_value'],
                    'reasoning': row['reasoning'],
                    'confidence': row['confidence']
                }
            
            # Get relationship context
            relationship = {}
            for row in conn.execute("""
                SELECT context_type, context_key, context_value, importance
                FROM relationship_context
                ORDER BY importance DESC, last_updated DESC
            """):
                if row['context_type'] not in relationship:
                    relationship[row['context_type']] = {}
                relationship[row['context_type']][row['context_key']] = {
                    'value': row['context_value'],
                    'importance': row['importance']
                }
            
            return {
                'personality_traits': traits,
                'personal_preferences': preferences,
                'relationship_context': relationship
            }
    
    def get_recent_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation insights."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            return [dict(row) for row in conn.execute("""
                SELECT * FROM conversation_insights 
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,))]
    
    def get_conversation_context(self) -> str:
        """Generate context about Seth for the LLM."""
        profile = self.get_personality_profile()
        
        context_parts = []
        
        # Personality traits
        if profile.get('personality_traits'):
            context_parts.append("**Seth's Personality:**")
            for category, traits in profile['personality_traits'].items():
                high_confidence_traits = [
                    f"{name}: {data['value']}" 
                    for name, data in traits.items() 
                    if data['confidence'] > 0.7
                ]
                if high_confidence_traits:
                    context_parts.append(f"- {category.title()}: {', '.join(high_confidence_traits)}")
        
        # Communication preferences
        if profile.get('relationship_context', {}).get('communication'):
            context_parts.append("\n**How Seth Communicates:**")
            comm = profile['relationship_context']['communication']
            for key, data in comm.items():
                if data['importance'] > 0.6:
                    context_parts.append(f"- {key.replace('_', ' ').title()}: {data['value']}")
        
        # Recent insights
        recent = self.get_recent_insights(5)
        if recent:
            context_parts.append("\n**Recent Conversation Insights:**")
            for insight in recent:
                if insight['confidence'] > 0.6:
                    context_parts.append(f"- {insight['insight']}")
        
        return "\n".join(context_parts) if context_parts else "Getting to know Seth..."
    
    def export_for_training(self) -> Dict[str, Any]:
        """Export all personal data for fine-tuning preparation."""
        profile = self.get_personality_profile()
        insights = self.get_recent_insights(100)  # More for training
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            conversations = [dict(row) for row in conn.execute("""
                SELECT * FROM conversation_history 
                ORDER BY timestamp DESC
            """)]
        
        return {
            'personality_profile': profile,
            'conversation_insights': insights,
            'conversation_history': conversations,
            'export_timestamp': datetime.now().isoformat()
        }


# Global instance
personal_memory = PersonalMemory()