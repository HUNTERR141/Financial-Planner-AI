from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import asyncio

from google.adk.runners import Runner
from google.genai.types import Content, Part
from app.api.deps import get_adk_runner

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_with_advisor(
    request: ChatRequest,
    runner: Runner = Depends(get_adk_runner)
):
    """
    Generically links the user to the orchestrator agent handling advice, settings, memory, etc.
    """
    try:
        content = Content(parts=[Part(text=request.query)], role="USER")
        response_parts = []

        async for event in runner.run_async(
            user_id="user",
            session_id="default",
            new_message=content,
        ):
            event_content = getattr(event, "content", None)
            if event_content is None:
                continue

            for part in getattr(event_content, "parts", []) or []:
                if getattr(part, "text", None):
                    response_parts.append(part.text)

        return {"response": "".join(response_parts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
