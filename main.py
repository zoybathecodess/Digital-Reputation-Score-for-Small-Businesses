"""
ScoreShield Backend API
FastAPI application for digital reputation scoring
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.fraud_detection import load_model, calculate_trust_score, create_features
from database.models import Seller, Review, TrustScore
from database.connection import get_database
from auth_routes import router as auth_router

app = FastAPI(
    title="ScoreShield API",
    description="Digital Reputation Scoring System for Small Online Sellers",
    version="1.0.0"
)

# Include auth routes
app.include_router(auth_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for ML models
fraud_model = None
label_encoders = None

@app.on_event("startup")
async def startup_event():
    """Load ML models on startup"""
    global fraud_model, label_encoders
    try:
        model_path = os.path.join(os.path.dirname(__file__), "models", "fraud_model.pkl")
        if os.path.exists(model_path):
            fraud_model, label_encoders = load_model(model_path)
            print("ML models loaded successfully")
        else:
            print("Warning: ML model not found. Please train the model first.")
    except Exception as e:
        print(f"Error loading ML models: {e}")

# Pydantic models for API
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

class SellerRequest(BaseModel):
    seller_id: str

class TrustScoreResponse(BaseModel):
    seller_id: str
    trust_score: float
    risk_level: str
    factors: Dict[str, Any]
    last_updated: datetime

class ReviewAnalysisResponse(BaseModel):
    review_id: str
    fraud_probability: float
    sentiment_analysis: Dict[str, Any]
    risk_factors: List[str]

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "ScoreShield API", "version": "1.0.0"}

@app.post("/analyze-review", response_model=ReviewAnalysisResponse)
async def analyze_review(review: ReviewData):
    """Analyze a single review for fraud detection"""
    if fraud_model is None:
        raise HTTPException(status_code=503, detail="ML model not loaded")

    try:
        # Prepare features for ML model
        features = create_features(pd.DataFrame([{
            'Rating': review.rating,
            'Review_Text': review.review_text,
            'Sentiment_Score': review.sentiment_score,
            'Verified_Purchase': 'Yes' if review.verified_purchase else 'No',
            'Delivery_Days': review.delivery_days,
            'IP_Review_Frequency': review.ip_review_frequency,
            'Device_Reuse_Count': review.device_reuse_count,
            'Platform': review.platform
        }]))

        # Get fraud prediction
        fraud_pred, fraud_prob = fraud_model.predict(features), fraud_model.predict_proba(features)

        # Analyze sentiment and risk factors
        risk_factors = []
        if fraud_prob[0][1] > 0.7:
            risk_factors.append("High fraud probability")
        if review.ip_review_frequency > 5:
            risk_factors.append("High IP review frequency")
        if review.device_reuse_count > 3:
            risk_factors.append("Device reuse detected")
        if not review.verified_purchase:
            risk_factors.append("Unverified purchase")

        sentiment_analysis = {
            "score": review.sentiment_score,
            "rating_match": abs(review.sentiment_score - review.rating/5) < 0.3
        }

        return ReviewAnalysisResponse(
            review_id=f"review_{review.seller_id}_{datetime.now().timestamp()}",
            fraud_probability=float(fraud_prob[0][1]),
            sentiment_analysis=sentiment_analysis,
            risk_factors=risk_factors
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/seller/{seller_id}/trust-score", response_model=TrustScoreResponse)
async def get_seller_trust_score(seller_id: str):
    """Get trust score for a seller"""
    if fraud_model is None:
        raise HTTPException(status_code=503, detail="ML model not loaded")

    try:
        # Load seller data (in production, this would come from database)
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ScoreShield_12000_Rows_With_Platforms.csv")
        df = pd.read_csv(data_path)

        # Filter reviews for this seller
        seller_reviews = df[df['Seller_ID'] == seller_id]

        if len(seller_reviews) == 0:
            raise HTTPException(status_code=404, detail="Seller not found")

        # Calculate trust score
        trust_score = calculate_trust_score(seller_reviews, fraud_model)

        # Determine risk level
        if trust_score >= 80:
            risk_level = "Low Risk"
        elif trust_score >= 60:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        # Calculate factors
        avg_rating = seller_reviews['Rating'].mean()
        verified_rate = (seller_reviews['Verified_Purchase'] == 'Yes').mean()
        complaint_rate = seller_reviews['Fraud_Label'].apply(lambda x: 1 if x != 'Genuine' else 0).mean()

        factors = {
            "total_reviews": len(seller_reviews),
            "average_rating": round(avg_rating, 2),
            "verified_purchase_rate": round(verified_rate * 100, 2),
            "complaint_rate": round(complaint_rate * 100, 2),
            "platform_distribution": seller_reviews['Platform'].value_counts().to_dict()
        }

        return TrustScoreResponse(
            seller_id=seller_id,
            trust_score=round(trust_score, 2),
            risk_level=risk_level,
            factors=factors,
            last_updated=datetime.now()
        )

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trust score calculation failed: {str(e)}")

@app.get("/sellers/top-rated")
async def get_top_rated_sellers(limit: int = 10):
    """Get top-rated sellers"""
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ScoreShield_12000_Rows_With_Platforms.csv")
        df = pd.read_csv(data_path)

        # Group by seller and calculate metrics
        seller_stats = df.groupby('Seller_ID').agg({
            'Rating': 'mean',
            'Review_ID': 'count',
            'Verified_Purchase': lambda x: (x == 'Yes').mean(),
            'Fraud_Label': lambda x: (x != 'Genuine').mean()
        }).round(2)

        seller_stats.columns = ['avg_rating', 'total_reviews', 'verified_rate', 'fraud_rate']

        # Filter sellers with minimum reviews
        seller_stats = seller_stats[seller_stats['total_reviews'] >= 5]

        # Calculate trust score approximation
        seller_stats['trust_score'] = (
            seller_stats['avg_rating'] * 0.4 +
            seller_stats['verified_rate'] * 0.3 +
            (1 - seller_stats['fraud_rate']) * 0.3
        ) * 25  # Scale to 0-100

        # Sort by trust score and return top sellers
        top_sellers = seller_stats.nlargest(limit, 'trust_score')

        return {
            "sellers": [
                {
                    "seller_id": seller_id,
                    "trust_score": round(row['trust_score'], 2),
                    "avg_rating": row['avg_rating'],
                    "total_reviews": int(row['total_reviews']),
                    "verified_rate": round(row['verified_rate'] * 100, 2)
                }
                for seller_id, row in top_sellers.iterrows()
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get top sellers: {str(e)}")

@app.get("/analytics/platform-stats")
async def get_platform_stats():
    """Get platform-wide statistics"""
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ScoreShield_12000_Rows_With_Platforms.csv")
        df = pd.read_csv(data_path)

        stats = {
            "total_reviews": len(df),
            "total_sellers": df['Seller_ID'].nunique(),
            "avg_rating": round(df['Rating'].mean(), 2),
            "fraud_rate": round((df['Fraud_Label'] != 'Genuine').mean() * 100, 2),
            "platform_distribution": df['Platform'].value_counts().to_dict(),
            "verified_purchase_rate": round((df['Verified_Purchase'] == 'Yes').mean() * 100, 2)
        }

        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get platform stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
