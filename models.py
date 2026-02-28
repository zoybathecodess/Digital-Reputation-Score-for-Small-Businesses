"""
Database models for ScoreShield
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    password_hash: str
    role: str  # 'seller' or 'customer'
    name: str
    seller_id: Optional[str] = None  # Only for sellers
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Seller(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    seller_id: str
    name: Optional[str] = None
    platform: str
    total_reviews: int = 0
    avg_rating: float = 0.0
    trust_score: float = 50.0
    risk_level: str = "Medium"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Review(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    review_id: str
    seller_id: str
    product_id: str
    rating: float
    review_text: str
    sentiment_score: float
    verified_purchase: bool
    delivery_days: int
    ip_review_frequency: int
    device_reuse_count: int
    platform: str
    fraud_probability: float = 0.0
    fraud_label: str = "Unknown"
    review_timestamp: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TrustScore(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    seller_id: str
    trust_score: float
    risk_level: str
    factors: Dict[str, Any]
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PlatformStats(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    total_reviews: int
    total_sellers: int
    avg_rating: float
    fraud_rate: float
    verified_purchase_rate: float
    platform_distribution: Dict[str, int]
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
