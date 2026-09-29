from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from app.config.constants import ALLOWED_CATEGORIES

class TransactionBase(BaseModel):
    amount: float = Field(..., allow_inf_nan=False)
    description: str = Field(..., min_length=1, max_length=500)
    category: Optional[str] = None
    date: str

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in ALLOWED_CATEGORIES:
            raise ValueError(f"category must be one of: {', '.join(ALLOWED_CATEGORIES)}")
        return value

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
