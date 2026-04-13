from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import asyncio

from google.adk.runners import Runner
from app.api.deps import get_adk_runner, get_db
from app.db.crud import get_transactions

router = APIRouter()

class TransactionChatRequest(BaseModel):
    message: str  # Example: "I just spent $55 on groceries"

@router.post("/", status_code=status.HTTP_201_CREATED)
async def process_transaction(
    request: TransactionChatRequest, 
    runner: Runner = Depends(get_adk_runner)
):
    """
    Receives natural language transaction logs and seamlessly delegates them to the AI agents.
    """
    try:
        # Offload sync ADK call to threadpool to preserve async API integrity
        response = await asyncio.to_thread(runner.run, request.message)
        return {"response": response, "agent_routed": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_raw_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Fetches raw history from the database directly, bypassing the AI processing layer.
    """
    try:
        txs = get_transactions(db, skip=skip, limit=limit)
        return txs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
