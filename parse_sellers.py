import pandas as pd
import json

df = pd.read_csv('data\\ScoreShield_12000_Rows_With_Platforms.csv')

# The dataset columns available are:
# Platform, Product_ID, Product_Category, Rating, Review_ID, Seller_ID, Review_Text, Review_Length, Sentiment_Score, Verified_Purchase, Product_Consistency, Device_ID, Activity_Frequency, Burst_Review_Flag, Fraud_Label

grouped = df.groupby(['Seller_ID', 'Platform'])

sellers = []
for (seller_id, platform), group in grouped:
    total_reviews = len(group)
    if total_reviews == 0:
        continue
        
    avg_rating = group['Rating'].mean()
    fakes = len(group[group['Fraud_Label'] == 'Fraud'])
    genuine = total_reviews - fakes
    complaints = len(group[group['Sentiment_Score'] < -0.3]) # Estimate complaints loosely based on negative sentiment mostly  
    verified_count = len(group[group['Verified_Purchase'] == 'Yes'])
    avg_sentiment = group['Sentiment_Score'].mean()

    # 1. Average Rating Score (Weight: 30%)
    rating_score = (avg_rating / 5.0) * 100

    # 2. Genuine Review Ratio (Weight: 25%)
    genuine_ratio = (genuine / total_reviews) * 100

    # 3. Complaint Penalty (Weight: 20%)
    complaint_ratio = complaints / total_reviews
    complaint_score = (1 - complaint_ratio) * 100

    # 4. Verified Purchase Ratio (Weight: 15%)
    verified_score = (verified_count / total_reviews) * 100

    # 5. Sentiment Score (Weight: 10%)
    # Sentiment is roughly -1 to 1 based on most models
    sentiment_score = ((avg_sentiment + 1) / 2.0) * 100

    # Final Trust Score
    trust_score = (0.30 * rating_score) + (0.25 * genuine_ratio) + (0.20 * complaint_score) + (0.15 * verified_score) + (0.10 * sentiment_score)
    trust_score = max(0, min(100, int(round(trust_score))))

    categories = group['Product_Category'].unique()[0] if len(group['Product_Category'].unique()) > 0 else "General"
    
    sellers.append({
        'id': seller_id,
        'sc': trust_score,
        'rt': round(avg_rating, 2),
        'rv': total_reviews,
        'pl': platform,
        'ct': categories,
        'fk': fakes,
        'co': complaints,
        'gn': genuine,
        'dl': 10.0 # Mock delivery time
    })

print(f"Total Unique Sellers extracted: {len(sellers)}")
with open('sellers_data.json', 'w') as f:
    json.dump(sellers, f)
