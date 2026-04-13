from sqlalchemy.orm import Session
from app.db import models
from app.schemas.transaction import TransactionCreate

def create_transaction(db: Session, transaction: TransactionCreate) -> models.DBTransaction:
    db_tx = models.DBTransaction(
        amount=transaction.amount,
        description=transaction.description,
        category=transaction.category,
        date=transaction.date
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBTransaction).offset(skip).limit(limit).all()

def update_transaction_category(db: Session, tx_id: int, category: str):
    tx = db.query(models.DBTransaction).filter(models.DBTransaction.id == tx_id).first()
    if tx:
        tx.category = category
        db.commit()
        db.refresh(tx)
    return tx
