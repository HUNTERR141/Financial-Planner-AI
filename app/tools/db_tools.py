from app.services.transaction_service import log_transaction

def add_transaction(amount: float, description: str, category: str = None) -> str:
    """
    Saves a financial transaction to the database.
    Always use this tool when the user states they spent or earned money.
    
    Args:
        amount: The exact monetary value from the input. Positive values mean spending; negative values mean income or refunds.
        description: A short blurb of what the transaction was.
        category: A higher level grouping (e.g. food, rent, entertainment). By default None if unknown.
        
    Returns:
        Structured response detailing how it was saved.
    """
    try:
        tx = log_transaction(amount=amount, description=description, category=category)
        return f"SUCCESS: Transaction saved. ID: {tx.id}, Amount: {tx.amount}, Desc: {tx.description}, Category: {tx.category}"
    except Exception as e:
        return "ERROR: Failed to save transaction."
