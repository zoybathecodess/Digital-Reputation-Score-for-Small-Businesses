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

```mermaid
graph TD;
    A[User Input] --> B[ Data Cleaning &           
 Preprocessing             
 - Remove nulls            
 - Fix datatypes           
 - Text normalization];

    B --> C[Sentiment Analysis VADER] ;
    C --> E[Sentiment Score -1 to +1 polarity] ;
    C --> F[Fake Review Detection XGB];

    F --> G[Fake Probability + Review Weight];
    F --> H[Seller-Level Aggregation:  
 - Weighted avg rating  
 - Weighted avg sentiment  
 - Review count  
 - Fake review ratio];
    

    H --> I[Bayesian Adjustment small seller correction];
    I --> J[Feature Normalization Scale features 0-1];
    J --> K[Digital Reputation Score Engine DRS           
 Combines:                                      
 - Bayesian rating                              
 - Sentiment quality                            
 - Authenticity score                           
 - Review volume confidence  ];

```
-----------------------------------------------------------------------------------------------
