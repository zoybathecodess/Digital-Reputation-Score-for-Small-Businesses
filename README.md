# Digital-Reputation-Score-for-Small-Businesses
🧩 **Overview**

  This project implements an AI-powered Digital Reputation Scoring (DRS) system designed to provide a fair and trustworthy evaluation of online sellers, with a focus on small businesses. 
  Traditional reputation systems rely heavily on average star ratings, making them vulnerable to fake or misleading reviews and disproportionately harmful to sellers with limited review volume. 
  To address this, the system combines:
  - sentiment analysis of review text
  - XGBoost-based fake review detection model that assigns a fraud probability to each review using behavioral, textual, and metadata features.
  Instead of removing suspicious reviews, their influence is reduced through probability-based weighting. Weighted ratings and sentiment are then aggregated at the seller level, normalized, and adjusted using Bayesian confidence modeling to account for low review counts.
**The final Digital Reputation Score integrates:**
- review quality
- emotional sentiment
- authenticity
- and confidence, resulting in an explainable, manipulation-resistant reputation framework that improves trust for both consumers and online marketplaces.

----------------------------------------------------------------------------------------------

🏗️ System Architecture

User / Dataset Input
(reviews, ratings, metadata)
        |
        v
+----------------------------+
| Data Cleaning & Validation |
| - Remove nulls             |
| - Fix datatypes            |
| - Normalize text           |
+----------------------------+
        |
        v
+----------------------------+        +-----------------------------+
| Sentiment Analysis Layer   | -----> | Sentiment Score             |
| (VADER)                    |        | (-1 to +1 polarity)         |
+----------------------------+        +-----------------------------+
        |
        v
+----------------------------+        +-----------------------------+
| Fake Review Detection      | -----> | Fake Probability            |
| (XGBoost Classifier)       |        | + Review Weight             |
+----------------------------+        +-----------------------------+
        |
        v
+----------------------------+
| Review Weighting Engine    |
| Genuine reviews ↑ weight  |
| Suspicious reviews ↓ weight|
+----------------------------+
        |
        v
+--------------------------------------------------+
| Seller-Level Aggregation                          |
| - Weighted average rating                         |
| - Weighted average sentiment                      |
| - Review count                                   |
| - Fake review ratio                               |
+--------------------------------------------------+
        |
        v
+----------------------------+        +-----------------------------+
| Bayesian Adjustment Layer  | -----> | Confidence-Aware Rating     |
| (Low-review correction)    |        | (Fair for small sellers)   |
+----------------------------+        +-----------------------------+
        |
        v
+----------------------------+
| Feature Normalization      |
| (Scale all signals to 0–1) |
+----------------------------+
        |
        v
+--------------------------------------------------+
| Digital Reputation Score (DRS Engine)             |
| Weighted combination of:                          |
| - Bayesian rating                                 |
| - Sentiment quality                               |
| - Authenticity score                              |
| - Review volume confidence                        |
+--------------------------------------------------+
        |
        v
+----------------------------+
| Reputation Classification |
| Low / Moderate / High      |
+----------------------------+
        |
        v
Final Output
(DRS Score, Label, Reports)
