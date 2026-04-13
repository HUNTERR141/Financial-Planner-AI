from app.services.categorization_service import auto_categorize_description, get_allowed_categories, update_category_in_db

def suggest_category(description: str) -> str:
    """Suggests a category for a transaction description using rule-based algorithmic matches."""
    return auto_categorize_description(description)

def list_allowed_categories() -> str:
    """Lists all allowed categories known to the system. Use this if AI-based categorization is needed."""
    cats = get_allowed_categories()
    return ", ".join(cats)

def apply_category(transaction_id: int, category: str) -> str:
    """Updates the transaction in the database with the provided category. Call this once the category is decided."""
    success = update_category_in_db(transaction_id, category)
    if success:
        return f"SUCCESS: Category '{category}' applied to transaction {transaction_id}."
    else:
        return f"ERROR: Failed to update transaction {transaction_id}. Not found."
