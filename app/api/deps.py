from typing import Generator
from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.main import main as create_runner
from google.adk.runners import Runner

DEFAULT_LOCAL_USER_ID = "local-user"


def get_current_user_id() -> str:
    """Return a single default user for local, single-user development."""
    return DEFAULT_LOCAL_USER_ID

def get_db() -> Generator[Session, None, None]:
    """Dependency injection for providing a safe database session to FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@lru_cache()
def get_adk_runner() -> Runner:
    """Dependency injection constructing and returning the singleton ADK Agent Runner."""
    return create_runner()
