from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class DailySummaryResponse(BaseModel):
    date: str
    total_orders: int
    total_revenue: float
    total_payments: int
    successful_payments: int
    failed_payments: int
    pending_payments: int
    platform_distribution: Dict[str, int]
    top_products: List[Dict[str, Any]]
    compliance_score: float
    fraud_alerts: int

class ComplianceMetricsResponse(BaseModel):
    total_checks: int
    passed_checks: int
    failed_checks: int
    compliance_rate: float
    risk_categories: Dict[str, int]
    recent_violations: List[Dict[str, Any]]
    recommendations: List[str]
