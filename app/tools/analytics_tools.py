from app.services.analytics_service import generate_analytics_report

def get_spending_analytics() -> str:
    """
    Generates a comprehensive spending analytics report.
    Returns a JSON string containing total spend, category breakdown (where you spent most), 
    and daily trend analysis with charts-ready data.
    Must be used anytime the user asks for spending breakdown, category-wise analysis, or trend detection.
    """
    try:
        report = generate_analytics_report()
        # Handle pydantic v1 vs v2
        if hasattr(report, "model_dump_json"):
            return report.model_dump_json()
        return report.json()
    except Exception as e:
        return f"ERROR: Failed to generate analytics. Details: {str(e)}"
