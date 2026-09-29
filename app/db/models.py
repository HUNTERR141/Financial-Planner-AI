from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class DBTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False, default="legacy")
    amount = Column(Float, nullable=False)
    description = Column(String, index=True)
    category = Column(String, index=True, nullable=True)
    date = Column(String, default=lambda: datetime.datetime.now().isoformat())
