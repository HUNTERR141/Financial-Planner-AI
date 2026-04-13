from app.memory.user_memory import save_insight_to_memory, get_all_insights_from_memory
from app.memory.context_manager import build_full_context, build_memory_context
from app.tools.analytics_tools import get_spending_analytics
from app.tools.forecasting_tools import get_future_forecast
import json

def get_raw_transaction_history() -> str:
    """
    Reads the raw DB transactions.
    Used exclusively by the Memory Agent to scan for patterns, anomalies, and risks over time.
    """
    from app.db.session import SessionLocal
    from app.db.models import DBTransaction
    db = SessionLocal()
    try:
        txs = db.query(DBTransaction).order_by(DBTransaction.date).all()
        if not txs:
            return "No transactions found."
            
        res = ["=== Raw Transaction Data ==="]
        for t in txs:
            res.append(f"{t.date[:10]} | ${t.amount:.2f} | {t.category} | {t.description}")
        return "\n".join(res)
    except Exception as e:
        return f"Database read error: {str(e)}"
    finally:
        db.close()

def save_financial_insight(insight_type: str, title: str, description: str) -> str:
    """
    Stores an observation in the memory intelligence layer.
    Use insight_type: 'habit', 'anomaly', or 'risk_alert'.
    """
    try:
        save_insight_to_memory(insight_type, title, description)
        return f"Successfully saved {insight_type.upper()}: {title}"
    except Exception as e:
        return f"ERROR: Could not save insight. Details: {str(e)}"

def get_intelligence_summary() -> str:
    """Returns the compiled abstract memory insights."""
    return build_memory_context()

def get_full_advisor_context() -> str:
    """Combines structured memory intelligence, live analytics, and live forecasts for the advisor."""
    try:
        analytics = get_spending_analytics()
        forecast  = get_future_forecast()
        return build_full_context(analytics, forecast)
    except Exception as e:
        return f"ERROR: Could not build full advisor context. Details: {str(e)}"

# Backwards compatibility endpoints for the Advisor agent
def recall_user_insights() -> str:
    return get_intelligence_summary()

def remember_insight(key: str, value: str) -> str:
    return save_financial_insight("habit", key, value)
