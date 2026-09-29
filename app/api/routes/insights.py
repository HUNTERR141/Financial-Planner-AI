import logging
from fastapi import APIRouter, Depends, HTTPException

from google.adk.runners import Runner
from google.genai.types import Content, Part
from app.api.deps import get_adk_runner, get_current_user_id
from app.context import user_context
from app.services.analytics_service import generate_analytics_report
from app.services.forecasting_service import generate_forecast

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def get_ai_insights(
    query: str = "Where did I spend most?", 
    runner: Runner = Depends(get_adk_runner),
    user_id: str = Depends(get_current_user_id),
):
    """
    Queries the intelligent agent layer to provide text-based contextual insights and recommendations.
    """
    try:
        content = Content(parts=[Part(text=query)], role="USER")
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

        return {"insights_report": "".join(response_parts)}
    except Exception:
        logger.exception("Insights agent request failed")
        raise HTTPException(status_code=500, detail="Unable to generate insights")

@router.get("/raw")
def get_raw_analytics(user_id: str = Depends(get_current_user_id)):
    """
    Securely fetches the structured raw data from the analytics models (bypassing AI).
    Useful for populating frontend charts explicitly.
    """
    try:
        analytics = generate_analytics_report(user_id=user_id)
        # Convert pydantic v1 vs v2 accurately
        if hasattr(analytics, "model_dump"):
            return analytics.model_dump()
        return analytics.dict()
    except Exception:
        logger.exception("Analytics request failed")
        raise HTTPException(status_code=500, detail="Unable to retrieve analytics")

@router.get("/forecast/raw")
def get_raw_forecast(user_id: str = Depends(get_current_user_id)):
    """
    Fetches purely statistical prediction data directly from the system model.
    """
    try:
        return generate_forecast(user_id=user_id)
    except Exception:
        logger.exception("Forecast request failed")
        raise HTTPException(status_code=500, detail="Unable to retrieve forecast")
