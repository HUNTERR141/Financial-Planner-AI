"""
context_manager.py
Compiles and manages the context sent to various agents (like Advisor),
translating raw insights into intelligent narrative structures.
"""
import json
from app.memory.user_memory import get_all_insights_from_memory

def build_memory_context() -> str:
    """Summarizes intelligence layer insights into a readable string."""
    insights = get_all_insights_from_memory()
    if not insights:
        return "No historical memory intelligence available."
        
    lines = ["=== Intelligence Layer Memory ==="]
    for ins in insights:
        type_banner = ins['insight_type'].upper()
        lines.append(f"[{type_banner}] {ins['title']}: {ins['description']}")
    return "\n".join(lines)

def build_full_context(analytics_json: str, forecast_json: str) -> str:
    """Combines live DB data (analytics/forecast) with structured memory intelligence."""
    memory_summary = build_memory_context()
    
    # Try to parse securely
    try:
        analytics = json.loads(analytics_json)
        top_cat = analytics.get('category_breakdown', [{}])[0].get('category', 'None')
        live_analytics = f"Total Spend: ${analytics.get('total_spend', 0)} | Top: {top_cat}"
    except Exception:
        live_analytics = analytics_json
        
    try:
        forecast = json.loads(forecast_json)
        predicted = forecast.get("predicted_next_month_spend", "N/A")
        model = forecast.get("model_used", "unknown")
        live_forecast = f"Predicted next month: ${predicted} (model: {model})"
    except Exception:
        live_forecast = forecast_json
        
    return f"{memory_summary}\n\n[LIVE ANALYTICS]\n{live_analytics}\n\n[LIVE FORECAST]\n{live_forecast}"
