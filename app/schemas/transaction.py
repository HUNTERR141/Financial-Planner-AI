from pydantic import BaseModel
from typing import Optional

class TransactionBase(BaseModel):
    amount: float
    description: str
    category: Optional[str] = None
    date: str

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int

    class Config:
        from_attributes = True
