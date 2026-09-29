import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from google.adk.runners import Runner
from google.genai.types import Content, Part
from app.api.deps import get_adk_runner, get_current_user_id, get_db
from app.db.crud import get_transactions
from app.context import user_context

logger = logging.getLogger(__name__)

router = APIRouter()

class TransactionChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def process_transaction(
    request: TransactionChatRequest, 
    runner: Runner = Depends(get_adk_runner),
    user_id: str = Depends(get_current_user_id),
):
    """
    Receives natural language transaction logs and seamlessly delegates them to the AI agents.
    """
    try:
        content = Content(parts=[Part(text=request.message)], role="USER")
        response_parts = []

        with user_context(user_id):
            async for event in runner.run_async(
                user_id=user_id,
                session_id=f"{user_id}:default",
                new_message=content,
            ):
                event_content = getattr(event, "content", None)
                if not event_content:
                    continue
                for part in getattr(event_content, "parts", []) or []:
                    if getattr(part, "text", None):
                        response_parts.append(part.text)

        return {"response": "".join(response_parts), "agent_routed": True}
    except Exception:
        logger.exception("Transaction agent request failed")
        raise HTTPException(status_code=500, detail="Unable to process transaction request")

@router.get("/")
def list_raw_transactions(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Fetches raw history from the database directly, bypassing the AI processing layer.
    """
    try:
        txs = get_transactions(db, user_id=user_id, skip=skip, limit=limit)
        return txs
    except Exception:
        logger.exception("Transaction history request failed")
        raise HTTPException(status_code=500, detail="Unable to retrieve transactions")
