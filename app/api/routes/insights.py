from fastapi import APIRouter, Depends, HTTPException
import asyncio

from google.adk.runners import Runner
from google.genai.types import Content, Part
from app.api.deps import get_adk_runner
from app.services.analytics_service import generate_analytics_report
from app.services.forecasting_service import generate_forecast

router = APIRouter()

@router.get("/")
async def get_ai_insights(
    query: str = "Where did I spend most?", 
    runner: Runner = Depends(get_adk_runner)
):
    """
    Queries the intelligent agent layer to provide text-based contextual insights and recommendations.
    """
    try:
        content = Content(parts=[Part(text=query)], role="USER")
        response_parts = []

        async for event in runner.run_async(
            user_id="user",
            session_id="default",
            new_message=content,
        ):
            event_content = getattr(event, "content", None)
            if not event_content:
                continue
            for part in getattr(event_content, "parts", []) or []:
                if getattr(part, "text", None):
                    response_parts.append(part.text)

        return {"insights_report": "".join(response_parts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/raw")
async def get_raw_analytics():
    """
    Securely fetches the structured raw data from the analytics models (bypassing AI).
    Useful for populating frontend charts explicitly.
    """
    try:
        analytics = generate_analytics_report()
        # Convert pydantic v1 vs v2 accurately
        if hasattr(analytics, "model_dump"):
            return analytics.model_dump()
        return analytics.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forecast/raw")
async def get_raw_forecast():
    """
    Fetches purely statistical prediction data directly from the system model.
    """
    try:
        return generate_forecast()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
