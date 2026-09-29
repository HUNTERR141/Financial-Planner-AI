"""
user_memory.py
Intelligence layer to store insights, patterns, and long-term user behavior.
Built with reusable APIs and a class structure to ensure future DB migration compatibility.
"""
from typing import Dict, List
from app.context import get_current_user_id

class InsightModel:
    def __init__(self, insight_type: str, title: str, description: str):
        self.insight_type = insight_type  # e.g., 'habit', 'anomaly', 'risk_alert'
        self.title = title
        self.description = description

class MemoryStore:
    def __init__(self):
        # Dictionary acts as our DB layer for now.
        # Prepared for an easy SQLAlchemy translation later
        self._db: Dict[str, Dict[str, InsightModel]] = {}
        
    def save(self, insight_type: str, title: str, description: str) -> None:
        user_id = get_current_user_id()
        if not user_id:
            raise ValueError("A user identity is required to save an insight")
        self._db.setdefault(user_id, {})[title] = InsightModel(insight_type, title, description)
        
    def get_all(self) -> List[InsightModel]:
        user_id = get_current_user_id()
        if not user_id:
            return []
        return list(self._db.get(user_id, {}).values())
        
    def clear(self):
        user_id = get_current_user_id()
        if user_id:
            self._db.pop(user_id, None)

# Global singleton representing active session memory
_memory_db = MemoryStore()

def save_insight_to_memory(insight_type: str, title: str, description: str) -> None:
    """Store an intelligence observation (habit, anomaly, risk)."""
    _memory_db.save(insight_type, title, description)

def get_all_insights_from_memory() -> List[Dict[str, str]]:
    """Retrieve all translated intelligence for downstream agents."""
    return [
        {
            "insight_type": i.insight_type,
            "title": i.title,
            "description": i.description
        } for i in _memory_db.get_all()
    ]

# Backwards compatibility wrappers for old advisor calls if needed
def save_insight(key: str, value: str):
    save_insight_to_memory("habit", key, value)

def get_all_insights() -> Dict[str, str]:
    return {i.title: i.description for i in _memory_db.get_all()}
