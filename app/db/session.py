from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from app.db.models import Base
from app.config.settings import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    columns = {column["name"] for column in inspect(engine).get_columns("transactions")}
    if "user_id" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE transactions ADD COLUMN user_id VARCHAR NOT NULL DEFAULT 'legacy'"))
