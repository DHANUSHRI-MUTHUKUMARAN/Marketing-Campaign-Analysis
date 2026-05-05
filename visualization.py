import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Setup ─────────────────────────────────────────────────────────────────────
df = pd.read_csv("processed_dataset.csv", parse_dates=['Date'])
os.makedirs("charts", exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 150

# ─────────────────────────────────────────
# CHART 1: Platform ROI Comparison (Bar)
# ─────────────────────────────────────────
channel = df.groupby('Channel_Used')['ROI'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#2ecc71' if x != 'Pinterest' else '#e74c3c' for x in channel['Channel_Used']]
bars = ax.bar(channel['Channel_Used'], channel['ROI'], color=colors, edgecolor='white', width=0.5)
ax.bar_label(bars, fmt='%.2f', padding=4, fontsize=11, fontweight='bold')
ax.set_title('Average ROI by Platform', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Platform', fontsize=12)
ax.set_ylabel('Average ROI', fontsize=12)
ax.set_ylim(0, channel['ROI'].max() * 1.2)
plt.tight_layout()
plt.savefig('charts/01_platform_roi.png')
plt.close()
print("✅ Chart 1 saved — Platform ROI")

# ─────────────────────────────────────────
# CHART 2: Platform CTR Comparison (Bar)
# ─────────────────────────────────────────
channel_ctr = df.groupby('Channel_Used')['CTR'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
colors2 = ['#3498db' if x != 'Pinterest' else '#e74c3c' for x in channel_ctr['Channel_Used']]
bars2 = ax.bar(channel_ctr['Channel_Used'], channel_ctr['CTR'], color=colors2, edgecolor='white', width=0.5)
ax.bar_label(bars2, fmt='%.2f%%', padding=4, fontsize=11, fontweight='bold')
ax.set_title('Average CTR by Platform', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Platform', fontsize=12)
ax.set_ylabel('Average CTR (%)', fontsize=12)
ax.set_ylim(0, channel_ctr['CTR'].max() * 1.2)
plt.tight_layout()
plt.savefig('charts/02_platform_ctr.png')
plt.close()
print("✅ Chart 2 saved — Platform CTR")

# ─────────────────────────────────────────
# CHART 3: Revenue vs Spend by Platform (Grouped Bar)
# ─────────────────────────────────────────
rev_spend = df.groupby('Channel_Used').agg(
    Total_Spend   = ('Acquisition_Cost', 'sum'),
    Total_Revenue = ('Estimated_Revenue', 'sum')
).reset_index()
rev_spend[['Total_Spend','Total_Revenue']] /= 1e9  # Convert to billions

x = range(len(rev_spend))
width = 0.35
fig, ax = plt.subplots(figsize=(9, 5))
b1 = ax.bar([i - width/2 for i in x], rev_spend['Total_Spend'],
            width, label='Total Spend ($B)', color='#e67e22')
b2 = ax.bar([i + width/2 for i in x], rev_spend['Total_Revenue'],
            width, label='Total Revenue ($B)', color='#2ecc71')
ax.bar_label(b1, fmt='$%.2fB', padding=3, fontsize=9)
ax.bar_label(b2, fmt='$%.2fB', padding=3, fontsize=9)
ax.set_xticks(list(x))
ax.set_xticklabels(rev_spend['Channel_Used'])
ax.set_title('Total Spend vs Revenue by Platform', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Amount (Billions $)', fontsize=12)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('charts/03_spend_vs_revenue.png')
plt.close()
print("✅ Chart 3 saved — Spend vs Revenue")

# ─────────────────────────────────────────
# CHART 4: Campaign Goal ROI by Platform (Heatmap)
# ─────────────────────────────────────────
goal_platform = df.groupby(['Channel_Used', 'Campaign_Goal'])['ROI'].mean().round(2).unstack()

fig, ax = plt.subplots(figsize=(9, 5))
sns.heatmap(goal_platform, annot=True, fmt='.2f', cmap='RdYlGn',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Avg ROI'})
ax.set_title('Campaign Goal × Platform — Average ROI', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Campaign Goal', fontsize=11)
ax.set_ylabel('Platform', fontsize=11)
plt.tight_layout()
plt.savefig('charts/04_goal_platform_heatmap.png')
plt.close()
print("✅ Chart 4 saved — Goal × Platform Heatmap")

# ─────────────────────────────────────────
# CHART 5: Customer Segment Conversion Rate (Bar)
# ─────────────────────────────────────────
seg = df.groupby('Customer_Segment')['Conversion_Rate_Pct'].mean().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
bars5 = ax.bar(seg['Customer_Segment'], seg['Conversion_Rate_Pct'],
               color='#9b59b6', edgecolor='white', width=0.5)
ax.bar_label(bars5, fmt='%.2f%%', padding=4, fontsize=11, fontweight='bold')
ax.set_title('Average Conversion Rate by Customer Segment', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Customer Segment', fontsize=12)
ax.set_ylabel('Conversion Rate (%)', fontsize=12)
ax.set_ylim(0, seg['Conversion_Rate_Pct'].max() * 1.2)
plt.tight_layout()
plt.savefig('charts/05_segment_conversion.png')
plt.close()
print("✅ Chart 5 saved — Segment Conversion")

# ─────────────────────────────────────────
# CHART 6: Campaign Duration vs CTR (Line)
# ─────────────────────────────────────────
dur = df.groupby('Duration_Days').agg(
    Avg_CTR = ('CTR', 'mean'),
    Avg_ROI = ('ROI', 'mean')
).reset_index()

fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()
ax1.plot(dur['Duration_Days'], dur['Avg_CTR'], 'o-', color='#3498db',
         linewidth=2.5, markersize=8, label='Avg CTR (%)')
ax2.plot(dur['Duration_Days'], dur['Avg_ROI'], 's--', color='#e74c3c',
         linewidth=2.5, markersize=8, label='Avg ROI')
ax1.set_xlabel('Campaign Duration (Days)', fontsize=12)
ax1.set_ylabel('Avg CTR (%)', color='#3498db', fontsize=12)
ax2.set_ylabel('Avg ROI', color='#e74c3c', fontsize=12)
ax1.set_title('Campaign Duration vs CTR and ROI', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks([15, 30, 45, 60])
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right')
plt.tight_layout()
plt.savefig('charts/06_duration_ctr_roi.png')
plt.close()
print("✅ Chart 6 saved — Duration vs CTR & ROI")

# ─────────────────────────────────────────
# CHART 7: Monthly ROI Trend (Line)
# ─────────────────────────────────────────
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
monthly = df.groupby('Month_Name')['ROI'].mean().reindex(month_order).reset_index()

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(monthly['Month_Name'], monthly['ROI'], 'o-', color='#1abc9c',
        linewidth=2.5, markersize=7)
ax.fill_between(monthly['Month_Name'], monthly['ROI'],
                alpha=0.15, color='#1abc9c')
for i, row in monthly.iterrows():
    ax.annotate(f"{row['ROI']:.2f}", (row['Month_Name'], row['ROI']),
                textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8)
ax.set_title('Monthly Average ROI Trend (All Platforms)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Average ROI', fontsize=12)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('charts/07_monthly_roi_trend.png')
plt.close()
print("✅ Chart 7 saved — Monthly ROI Trend")

# ─────────────────────────────────────────
# CHART 8: Correlation Heatmap
# ─────────────────────────────────────────
corr_cols = ['CTR', 'Conversion_Rate_Pct', 'ROI',
             'CPC', 'CPM', 'Acquisition_Cost', 'Engagement_Score']
corr = df[corr_cols].corr().round(2)

fig, ax = plt.subplots(figsize=(9, 7))
mask = pd.DataFrame(False, index=corr.index, columns=corr.columns)
for i in range(len(corr)):
    for j in range(i):
        mask.iloc[i, j] = True
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, linewidths=0.5, ax=ax, mask=mask,
            cbar_kws={'label': 'Correlation'})
ax.set_title('Metric Correlation Heatmap', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('charts/08_correlation_heatmap.png')
plt.close()
print("✅ Chart 8 saved — Correlation Heatmap")

# ─────────────────────────────────────────
# CHART 9: CPC vs ROI Scatter (by Platform)
# ─────────────────────────────────────────
sample = df.sample(n=5000, random_state=42)
platform_colors = {
    'Instagram': '#e91e8c',
    'Facebook':  '#3b5998',
    'Twitter':   '#1da1f2',
    'Pinterest': '#e60023'
}

fig, ax = plt.subplots(figsize=(9, 6))
for platform, grp in sample.groupby('Channel_Used'):
    ax.scatter(grp['CPC'], grp['ROI'],
               alpha=0.3, s=15,
               color=platform_colors[platform],
               label=platform)
ax.set_title('CPC vs ROI by Platform (Sample 5,000)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Cost Per Click ($)', fontsize=12)
ax.set_ylabel('ROI', fontsize=12)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('charts/09_cpc_vs_roi_scatter.png')
plt.close()
print("✅ Chart 9 saved — CPC vs ROI Scatter")

# ─────────────────────────────────────────
# CHART 10: Location ROI Comparison (Horizontal Bar)
# ─────────────────────────────────────────
loc = df.groupby('Location')['ROI'].mean().sort_values().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
bars10 = ax.barh(loc['Location'], loc['ROI'],
                 color='#f39c12', edgecolor='white')
ax.bar_label(bars10, fmt='%.2f', padding=4, fontsize=11, fontweight='bold')
ax.set_title('Average ROI by Location', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Average ROI', fontsize=12)
ax.set_xlim(0, loc['ROI'].max() * 1.15)
plt.tight_layout()
plt.savefig('charts/10_location_roi.png')
plt.close()
print("✅ Chart 10 saved — Location ROI")

print("\n🎉 All 10 charts saved to /charts folder")
print("📁 Open the charts/ folder to review all visualizations")