# Marketing Campaign Analysis (Instagram Ads)

---

## Project Overview
This project analyzes social media advertising campaigns to evaluate performance using key metrics such as **Click-Through Rate (CTR)** and **Conversion Rate**. The goal is to identify high-performing campaigns and understand factors affecting their success.
In addition, an interactive dashboard is built to visualize insights and support data-driven decision-making.

---

## Problem Statement
Analyze Instagram ad campaigns to evaluate performance using CTR and Conversion Rate, and identify which campaigns perform best.

---

## Objectives
- Compare campaign performance across platforms
- Identify high-performing advertisements
- Understand the impact of audience and customer segments
- Suggest improvements for campaign optimization

---

## Dataset Information
- Total Records: 300,000
- Initial Features: 16 columns
- Enhanced Features: 25 columns (after preprocessing)
- Large-scale dataset suitable for analytics and ML

---

## Channels Used
- Instagram
- Facebook
- Pinterest
- Twitter

--- 

## Campaign Goals
- Product Launch
- Market Expansion
- Increase Sales
- Brand Awareness

---

## Customer Segments
- Health
- Home
- Technology
- Food
- Fashion

---

## Dataset Scope
US-based dataset covering multiple cities
 
---

## Data Preprocessing

### Feature Engineering
The dataset was enhanced from 16 → 25 columns by adding:

**Time-Based Features**
- Month, Quarter, Month_Name
    → Used for analyzing seasonal trends
**Duration Conversion**
- Duration_Days
    → Converted text values into numeric format
**Performance Metrics**
- **CTR (Click-Through Rate)**: Measures engagement efficiency
- **CPC (Cost Per Click)**: Cost per user click
- **CPM (Cost Per 1000 Impressions)**: Advertising cost efficiency
- **Conversion_Rate_Pct**: Conversion rate in percentage
- **Estimated_Revenue**: Approximate campaign earnings

---

## Sanity Checks (Data Validation)
- CTR = Clicks / Impressions × 100
    - Range: 15% → 33%
    - Observation: Values are very similar across campaigns
- ROI = Profit / Cost
    - Range: 0 → 8
    - Negative values: 0
    - Observation: All campaigns are profitable → not fully realistic
- CPC (Cost Per Click)
    - Range: 0.24 → 1.71
    - Observation: Moderate variation
- Missing Values: None

---

## Dataset Characteristics
- All categories are evenly distributed:
    - Channels (~75K each)
    - Campaign Goals (~75K each)
    - Customer Segments (~60K each)
    - Duration (equal distribution)

→ Indicates a highly balanced dataset (possibly synthetic)

---

## Exploratory Data Analysis (EDA)
**Overall Performance**
- Total Campaigns: 300,000
- Total Spend: $2.3 Billion
- Total Revenue: $9.7 Billion
- Average ROI: 3.18
- Average CTR: 31.4%

→ Campaigns are generally profitable

---

## Platform Performance
**Best Platforms**
- Instagram → ROI ≈ 4.01
- Twitter → ROI ≈ 4.00
- Facebook → ROI ≈ 3.99
**Weak Platform**
- Pinterest → ROI ≈ 0.72

→ Pinterest performs significantly worse than other platforms

---

## Campaign Goals & Customer Segments
- Performance remains almost identical across all categories

→ Minimal impact on ROI and CTR

---

## Duration Analysis
- Longer campaigns → slightly higher CTR

→ Indicates duration has a small positive impact

---

## Dashboard (UI)

An interactive dashboard was developed using Streamlit to visualize campaign performance and insights.

**Features**
- Platform-wise ROI and CTR comparison
- Spend vs Revenue analysis
- Campaign goal and customer segment insights
- Heatmaps (Platform × Goal / Segment / Location)
- Monthly trend analysis
- CPC vs ROI relationship
- Duration vs CTR & ROI
- Budget reallocation simulation
- Top and bottom campaign identification

---

## Key Insights
- Platform choice strongly affects campaign performance
- Higher CPC leads to lower ROI (cost impacts profitability)
- CTR has limited variation across campaigns
- Campaign goals and customer segments show minimal influence
- Pinterest consistently underperforms across all metrics
- Budget reallocation can significantly increase revenue

---

## Project Status
- Dataset cleaned and preprocessed
- Feature engineering completed
- EDA performed across all platforms
- Interactive dashboard developed
- Ready for visualization and machine learning