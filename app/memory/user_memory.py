"""
user_memory.py
Intelligence layer to store insights, patterns, and long-term user behavior.
Built with reusable APIs and a class structure to ensure future DB migration compatibility.
"""
from typing import Dict, List

class InsightModel:
    def __init__(self, insight_type: str, title: str, description: str):
        self.insight_type = insight_type  # e.g., 'habit', 'anomaly', 'risk_alert'
        self.title = title
        self.description = description

class MemoryStore:
    def __init__(self):
        # Dictionary acts as our DB layer for now.
        # Prepared for an easy SQLAlchemy translation later
        self._db: Dict[str, InsightModel] = {}
        
    def save(self, insight_type: str, title: str, description: str) -> None:
        self._db[title] = InsightModel(insight_type, title, description)
        
    def get_all(self) -> List[InsightModel]:
        return list(self._db.values())
        
    def clear(self):
        self._db.clear()

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
