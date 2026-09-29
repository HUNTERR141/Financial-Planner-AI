import json
import os
from app.db.session import SessionLocal
from app.db.crud import update_transaction_category
from app.context import get_current_user_id
from app.config.constants import ALLOWED_CATEGORIES

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/categories.json")

def load_category_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def auto_categorize_description(description: str) -> str:
    """Rule-based categorization against predefined keywords."""
    data = load_category_data()
    rules = data.get("rules", {})
    desc_lower = description.lower()
    
    for keyword, category in rules.items():
        if keyword in desc_lower:
            return category
            
    return "UNKNOWN"

def get_allowed_categories():
    data = load_category_data()
    return data.get("categories", [])

def update_category_in_db(transaction_id: int, new_category: str) -> bool:
    """Service bridge to update the database"""
    if new_category not in ALLOWED_CATEGORIES:
        return False
    user_id = get_current_user_id()
    if not user_id:
        return False
    db = SessionLocal()
    try:
        tx = update_transaction_category(db, transaction_id, new_category, user_id)
        return tx is not None
    finally:
        db.close()
