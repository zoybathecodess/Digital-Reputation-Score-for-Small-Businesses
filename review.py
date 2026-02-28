from pydantic import BaseModel
from typing import List

class ReviewData(BaseModel):
    seller_id: str
    rating: float
    review_text: str
    sentiment_score: float
    verified_purchase: bool
    delivery_days: int
    ip_review_frequency: int
    device_reuse_count: int
    platform: str

class ReviewAnalysisResponse(BaseModel):
    review_id: str
    fraud_probability: float
    sentiment_analysis: dict
    risk_factors: List[str]
