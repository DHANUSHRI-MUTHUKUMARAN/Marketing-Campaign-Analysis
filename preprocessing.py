import pandas as pd

# ── Load clean dataset ────────────────────────────────────────────────────────
df = pd.read_csv("clean_dataset.csv", parse_dates=['Date'])

# ─────────────────────────────────────────
# STEP 1: Fix Duration column
# ─────────────────────────────────────────
print("Duration samples:", df['Duration'].unique())
df['Duration_Days'] = df['Duration'].str.extract(r'(\d+)').astype(int)

# ─────────────────────────────────────────
# STEP 2: Scale Conversion_Rate to percentage
# ─────────────────────────────────────────
df['Conversion_Rate_Pct'] = df['Conversion_Rate'] * 100

# ─────────────────────────────────────────
# STEP 3: Add derived metrics
# ─────────────────────────────────────────

# CPC — Cost Per Click
df['CPC'] = df['Acquisition_Cost'] / df['Clicks']

# CPM — Cost Per 1000 Impressions
df['CPM'] = (df['Acquisition_Cost'] / df['Impressions']) * 1000

# Estimated Revenue (reverse from ROI)
# ROI = (Revenue - Cost) / Cost  →  Revenue = Cost * (1 + ROI)
df['Estimated_Revenue'] = df['Acquisition_Cost'] * (1 + df['ROI'])

# ─────────────────────────────────────────
# STEP 4: Add time features
# ─────────────────────────────────────────
df['Month']      = df['Date'].dt.month
df['Quarter']    = df['Date'].dt.quarter
df['Month_Name'] = df['Date'].dt.strftime('%B')

# ─────────────────────────────────────────
# STEP 5: Sanity checks
# ─────────────────────────────────────────
print("\n--- Sanity Checks ---")
print("CTR range        :", df['CTR'].min().round(2), "→", df['CTR'].max().round(2))
print("ROI range        :", df['ROI'].min().round(2), "→", df['ROI'].max().round(2))
print("CPC range        :", df['CPC'].min().round(2), "→", df['CPC'].max().round(2))
print("Negative ROI     :", (df['ROI'] < 0).sum())
print("Missing Values   :\n", df.isnull().sum())

# ─────────────────────────────────────────
# STEP 6: Summary breakdown
# ─────────────────────────────────────────
print("\n--- Channel-wise Record Count ---")
print(df['Channel_Used'].value_counts())

print("\n--- Campaign Goal Distribution ---")
print(df['Campaign_Goal'].value_counts())

print("\n--- Customer Segment Distribution ---")
print(df['Customer_Segment'].value_counts())

print("\n--- Duration Distribution ---")
print(df['Duration'].value_counts().sort_index())

# ─────────────────────────────────────────
# STEP 7: Save single processed dataset (all platforms)
# ─────────────────────────────────────────
df.to_csv("processed_dataset.csv", index=False)
print("\n✅ processed_dataset.csv saved — all 4 platforms included")
print(f"   Total records : {len(df):,}")
print(f"   Total columns : {len(df.columns)}")
print(f"\n   Columns added : Duration_Days, Conversion_Rate_Pct,")
print(f"                   CPC, CPM, Estimated_Revenue,")
print(f"                   Month, Quarter, Month_Name")