from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class CategoryAnalysis(BaseModel):
    category: str
    total_amount: float
    percentage: float

class TrendDataPoint(BaseModel):
    date: str
    amount: float

class TrendAnalysis(BaseModel):
    trends: List[TrendDataPoint]
    average_daily_spend: float
    highest_spend_day: Optional[str]

class AnalyticsReport(BaseModel):
    total_spend: float
    category_breakdown: List[CategoryAnalysis]
    trend_analysis: TrendAnalysis
    charts_ready_data: Dict[str, Any]
