import datetime
from app.db.session import SessionLocal, init_db
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.db.crud import create_transaction
from app.context import get_current_user_id

# Ensure database tables exist automatically locally
init_db()


def log_transaction(amount: float, description: str, category: str = None, date_str: str = None, user_id: str = None) -> TransactionRead:
    """Business logic to process and store a new transaction for the local single-user app."""
    db = SessionLocal()
    try:
        if not date_str:
            date_str = datetime.datetime.now().isoformat()

        tx_create = TransactionCreate(
            amount=amount,
            description=description,
            category=category,
            date=date_str
        )

        owner_id = user_id or get_current_user_id()
        db_tx = create_transaction(db, tx_create, owner_id)
        return TransactionRead.model_validate(db_tx)
    finally:
        db.close()
