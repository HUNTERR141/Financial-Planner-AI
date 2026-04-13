from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class DBTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, index=True)
    category = Column(String, index=True, nullable=True)
    date = Column(String, default=lambda: datetime.datetime.now().isoformat())
