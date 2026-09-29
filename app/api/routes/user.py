import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from google.adk.runners import Runner
from google.genai.types import Content, Part
from app.api.deps import get_adk_runner, get_current_user_id
from app.context import user_context

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)

@router.post("/chat")
async def chat_with_advisor(
    request: ChatRequest,
    runner: Runner = Depends(get_adk_runner),
    user_id: str = Depends(get_current_user_id),
):
    """
    Generically links the user to the orchestrator agent handling advice, settings, memory, etc.
    """
    try:
        content = Content(parts=[Part(text=request.query)], role="USER")
        response_parts = []

        with user_context(user_id):
            async for event in runner.run_async(
                user_id=user_id,
                session_id=f"{user_id}:default",
                new_message=content,
            ):
                event_content = getattr(event, "content", None)
                if event_content is None:
                    continue

                for part in getattr(event_content, "parts", []) or []:
                    if getattr(part, "text", None):
                        response_parts.append(part.text)

        return {"response": "".join(response_parts)}
    except Exception:
        logger.exception("Advisor request failed")
        raise HTTPException(status_code=500, detail="Unable to process advisor request")
