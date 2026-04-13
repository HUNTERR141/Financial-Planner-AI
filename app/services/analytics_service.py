from collections import defaultdict
from typing import List, Dict, Any
from app.db.session import SessionLocal
from app.db.models import DBTransaction
from app.schemas.insights import AnalyticsReport, CategoryAnalysis, TrendAnalysis, TrendDataPoint

def generate_analytics_report() -> AnalyticsReport:
    db = SessionLocal()
    try:
        transactions = db.query(DBTransaction).all()
        
        total_spend = sum(t.amount for t in transactions if t.amount > 0) # Assumes positive amount is spend, or adjust based on logic
        
        category_totals = defaultdict(float)
        date_totals = defaultdict(float)
        
        for t in transactions:
            cat = t.category if t.category else "Uncategorized"
            category_totals[cat] += t.amount
            
            # Simple date grouping by YYYY-MM-DD
            date_str = t.date[:10] if getattr(t, "date", None) else "Unknown"
            date_totals[date_str] += t.amount
            
        category_breakdown = []
        charts_category_data = []
        for cat, amt in category_totals.items():
            pct = (amt / total_spend * 100) if total_spend > 0 else 0.0
            category_breakdown.append(CategoryAnalysis(category=cat, total_amount=amt, percentage=pct))
            charts_category_data.append({"name": cat, "value": amt})
            
        category_breakdown.sort(key=lambda x: x.total_amount, reverse=True)
        
        # Trends
        trends = []
        charts_trend_data = []
        highest_spend_day = None
        highest_spend = -1.0
        
        for date_str in sorted(date_totals.keys()):
            amt = date_totals[date_str]
            trends.append(TrendDataPoint(date=date_str, amount=amt))
            charts_trend_data.append({"date": date_str, "amount": amt})
            if amt > highest_spend:
                highest_spend = amt
                highest_spend_day = date_str
                
        num_days = len(date_totals)
        avg_spend = total_spend / num_days if num_days > 0 else 0.0
        
        trend_analysis = TrendAnalysis(
            trends=trends,
            average_daily_spend=avg_spend,
            highest_spend_day=highest_spend_day
        )
        
        charts_ready_data = {
            "category_distribution": charts_category_data,
            "daily_trends": charts_trend_data
        }
        
        return AnalyticsReport(
            total_spend=total_spend,
            category_breakdown=category_breakdown,
            trend_analysis=trend_analysis,
            charts_ready_data=charts_ready_data
        )
    finally:
        db.close()
