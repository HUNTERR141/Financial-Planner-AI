import json
from app.services.forecasting_service import generate_forecast

def get_future_forecast() -> str:
    """
    Predicts future expenses and monthly trends based on historical transaction data.
    Use this tool when the user asks questions like "How much will I spend next month?"
    or "What is my forecast?".
    
    Returns:
        A JSON string containing predicted next month spend, category breakdown, 
        and the forecasting model used.
    """
    try:
        forecast_data = generate_forecast()
        return json.dumps(forecast_data, indent=2)
    except Exception as e:
        return "ERROR: Failed to generate forecast."
