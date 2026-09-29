import datetime
from collections import defaultdict
from app.db.session import SessionLocal
from app.db.models import DBTransaction
from app.context import get_current_user_id

def generate_forecast(user_id: str = None) -> dict:
    db = SessionLocal()
    try:
        owner_id = user_id or get_current_user_id()
        if not owner_id:
            raise ValueError("A user identity is required to generate a forecast")
        transactions = (db.query(DBTransaction)
                        .filter(DBTransaction.user_id == owner_id, DBTransaction.amount > 0)
                        .all())
        if not transactions:
            return {
                "predicted_next_month_spend": 0.0,
                "predicted_category_breakdown": {},
                "historical_monthly_spend": {},
                "model_used": "none",
                "message": "Not enough data to generate forecast."
            }
        
        # Group by YYYY-MM
        monthly_spend = defaultdict(float)
        for t in transactions:
            month = t.date[:7] if t.date else "Unknown"
            if month != "Unknown":
                monthly_spend[month] += t.amount
                
        sorted_months = sorted(monthly_spend.keys())
        
        # If we have multiple months, simple moving average of the last 3 months
        if len(sorted_months) >= 2:
            last_3_months = sorted_months[-3:]
            total_last_months = sum(monthly_spend[m] for m in last_3_months)
            avg_monthly_spend = total_last_months / len(last_3_months)
            model = f"SMA_{len(last_3_months)}_months"
        else:
            # Only one month of data. Let's do daily average scaled to 30 days.
            daily_spend = defaultdict(float)
            for t in transactions:
                day = t.date[:10] if t.date else "Unknown"
                if day != "Unknown":
                    daily_spend[day] += t.amount
                    
            days_count = len(daily_spend)
            total_spend = sum(daily_spend.values())
            
            if days_count > 0:
                avg_daily = total_spend / days_count
                avg_monthly_spend = avg_daily * 30
                model = "daily_average_scaled"
            else:
                avg_monthly_spend = total_spend
                model = "raw_fallback"
                
        # Category-wise simple forecast
        category_monthly_spend = defaultdict(lambda: defaultdict(float))
        for t in transactions:
            month = t.date[:7] if t.date else "Unknown"
            cat = t.category if t.category else "Uncategorized"
            if month != "Unknown":
                category_monthly_spend[cat][month] += t.amount
                
        category_forecasts = {}
        for cat, months_data in category_monthly_spend.items():
            cat_months = sorted(months_data.keys())
            if len(cat_months) >= 2:
                last_3 = cat_months[-3:]
                cat_avg = sum(months_data[m] for m in last_3) / len(last_3)
            else:
                cat_avg = sum(months_data.values())
            category_forecasts[cat] = cat_avg

        category_total = sum(category_forecasts.values())
        if category_total > 0:
            category_forecasts = {
                category: value * avg_monthly_spend / category_total
                for category, value in category_forecasts.items()
            }
                
        return {
            "predicted_next_month_spend": round(avg_monthly_spend, 2),
            "predicted_category_breakdown": {k: round(v, 2) for k, v in category_forecasts.items()},
            "historical_monthly_spend": dict(monthly_spend),
            "model_used": model
        }
    finally:
        db.close()
