import pandas as pd

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv("processed_dataset.csv", parse_dates=['Date'])

print("="*60)
print("MARKETING CAMPAIGN ANALYSIS — WEEK 3 EDA")
print("="*60)

# ─────────────────────────────────────────
# ANALYSIS 0: Full Dataset Overview
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 0: Full Dataset Summary")
print(f"Total Campaigns  : {len(df):,}")
print(f"Total Spend      : ${df['Acquisition_Cost'].sum():,.0f}")
print(f"Total Revenue    : ${df['Estimated_Revenue'].sum():,.0f}")
print(f"Overall Avg ROI  : {df['ROI'].mean():.2f}")
print(f"Overall Avg CTR  : {df['CTR'].mean():.2f}%")
print(f"Overall Avg CPC  : ${df['CPC'].mean():.2f}")
print(f"Date Range       : {df['Date'].min().date()} → {df['Date'].max().date()}")

# ─────────────────────────────────────────
# ANALYSIS 1: Channel Comparison
# Which platform performs best?
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 1: Platform Performance Comparison")
channel = df.groupby('Channel_Used').agg(
    Avg_CTR        = ('CTR', 'mean'),
    Avg_Conversion = ('Conversion_Rate_Pct', 'mean'),
    Avg_ROI        = ('ROI', 'mean'),
    Avg_CPC        = ('CPC', 'mean'),
    Avg_CPM        = ('CPM', 'mean'),
    Total_Spend    = ('Acquisition_Cost', 'sum'),
    Total_Revenue  = ('Estimated_Revenue', 'sum'),
    Campaign_Count = ('Campaign_ID', 'count')
).round(2)
channel['Revenue_Per_Dollar'] = (
    channel['Total_Revenue'] / channel['Total_Spend']
).round(2)
print(channel.sort_values('Avg_ROI', ascending=False).to_string())

# ─────────────────────────────────────────
# ANALYSIS 2: Campaign Goal Performance
# (across all platforms)
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 2: Campaign Goal Performance (All Platforms)")
goal = df.groupby('Campaign_Goal').agg(
    Avg_CTR        = ('CTR', 'mean'),
    Avg_Conversion = ('Conversion_Rate_Pct', 'mean'),
    Avg_ROI        = ('ROI', 'mean'),
    Avg_CPC        = ('CPC', 'mean'),
    Count          = ('Campaign_ID', 'count')
).round(2)
print(goal.sort_values('Avg_ROI', ascending=False).to_string())

# ─────────────────────────────────────────
# ANALYSIS 3: Campaign Goal × Platform
# Which goal works best on which platform?
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 3: Campaign Goal × Platform (Avg ROI)")
goal_channel = df.groupby(['Channel_Used', 'Campaign_Goal'])['ROI'].mean().round(2).unstack()
print(goal_channel.to_string())

# ─────────────────────────────────────────
# ANALYSIS 4: Customer Segment Performance
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 4: Customer Segment Performance (All Platforms)")
seg = df.groupby('Customer_Segment').agg(
    Avg_CTR        = ('CTR', 'mean'),
    Avg_Conversion = ('Conversion_Rate_Pct', 'mean'),
    Avg_ROI        = ('ROI', 'mean'),
    Avg_CPC        = ('CPC', 'mean')
).round(2)
print(seg.sort_values('Avg_Conversion', ascending=False).to_string())

# ─────────────────────────────────────────
# ANALYSIS 5: Segment × Platform
# Which segment performs best on which platform?
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 5: Customer Segment × Platform (Avg Conversion Rate %)")
seg_channel = df.groupby(['Channel_Used', 'Customer_Segment'])['Conversion_Rate_Pct'].mean().round(2).unstack()
print(seg_channel.to_string())

# ─────────────────────────────────────────
# ANALYSIS 6: Location Performance
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 6: Location Performance (All Platforms)")
loc = df.groupby('Location').agg(
    Avg_ROI        = ('ROI', 'mean'),
    Avg_CTR        = ('CTR', 'mean'),
    Avg_Conversion = ('Conversion_Rate_Pct', 'mean'),
    Avg_CPC        = ('CPC', 'mean'),
    Total_Spend    = ('Acquisition_Cost', 'sum')
).round(2)
print(loc.sort_values('Avg_ROI', ascending=False).to_string())

# ─────────────────────────────────────────
# ANALYSIS 7: Duration Impact
# Do longer campaigns perform better?
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 7: Campaign Duration vs Performance")
dur = df.groupby('Duration').agg(
    Avg_CTR        = ('CTR', 'mean'),
    Avg_Conversion = ('Conversion_Rate_Pct', 'mean'),
    Avg_ROI        = ('ROI', 'mean'),
    Avg_CPC        = ('CPC', 'mean'),
    Count          = ('Campaign_ID', 'count')
).round(2)
print(dur.sort_values('Avg_ROI', ascending=False).to_string())

# ─────────────────────────────────────────
# ANALYSIS 8: Monthly Trend
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 8: Monthly Performance Trend (All Platforms)")
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
monthly = df.groupby('Month_Name').agg(
    Avg_ROI        = ('ROI', 'mean'),
    Avg_CTR        = ('CTR', 'mean'),
    Avg_Conversion = ('Conversion_Rate_Pct', 'mean'),
    Campaign_Count = ('Campaign_ID', 'count')
).round(2)
monthly = monthly.reindex([m for m in month_order if m in monthly.index])
print(monthly.to_string())

# ─────────────────────────────────────────
# ANALYSIS 9: Quarterly Trend
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 9: Quarterly Performance Trend")
quarterly = df.groupby('Quarter').agg(
    Avg_ROI        = ('ROI', 'mean'),
    Avg_CTR        = ('CTR', 'mean'),
    Avg_Conversion = ('Conversion_Rate_Pct', 'mean'),
    Total_Spend    = ('Acquisition_Cost', 'sum'),
    Total_Revenue  = ('Estimated_Revenue', 'sum'),
    Campaign_Count = ('Campaign_ID', 'count')
).round(2)
print(quarterly.to_string())

# ─────────────────────────────────────────
# ANALYSIS 10: Top 10 Best Campaigns (by ROI)
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 10: Top 10 Campaigns by ROI")
top10 = df.nlargest(10, 'ROI')[
    ['Campaign_ID', 'Channel_Used', 'Campaign_Goal',
     'Customer_Segment', 'Location', 'Duration',
     'ROI', 'CTR', 'Conversion_Rate_Pct', 'CPC']
].round(2)
print(top10.to_string())

# ─────────────────────────────────────────
# ANALYSIS 11: Bottom 10 Campaigns (by ROI)
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 11: Bottom 10 Campaigns by ROI")
bot10 = df.nsmallest(10, 'ROI')[
    ['Campaign_ID', 'Channel_Used', 'Campaign_Goal',
     'Customer_Segment', 'Location', 'Duration',
     'ROI', 'CTR', 'Conversion_Rate_Pct', 'CPC']
].round(2)
print(bot10.to_string())

# ─────────────────────────────────────────
# ANALYSIS 12: Correlation Matrix
# ─────────────────────────────────────────
print("\n📊 ANALYSIS 12: Metric Correlations")
corr_cols = ['CTR', 'Conversion_Rate_Pct', 'ROI',
             'CPC', 'CPM', 'Acquisition_Cost',
             'Engagement_Score', 'Duration_Days']
print(df[corr_cols].corr().round(2).to_string())

print("\n✅ Week 3 EDA Complete — All 4 Platforms Analyzed")