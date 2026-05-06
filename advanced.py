import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ── Setup ─────────────────────────────────────────────────────────────────────
df = pd.read_csv("processed_dataset.csv", parse_dates=['Date'])
os.makedirs("charts", exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.dpi'] = 150

print("="*60)
print("MARKETING CAMPAIGN ANALYSIS — WEEK 5 ADVANCED")
print("="*60)

# ─────────────────────────────────────────
# ADVANCED 1: Platform × Duration
# Which duration works best per platform?
# ─────────────────────────────────────────
print("\n📊 ADVANCED 1: Platform × Duration (Avg ROI)")
plat_dur = df.groupby(['Channel_Used', 'Duration'])['ROI'].mean().round(2).unstack()
print(plat_dur.to_string())

# Chart
fig, ax = plt.subplots(figsize=(10, 5))
plat_dur.plot(kind='bar', ax=ax, edgecolor='white', width=0.7)
ax.set_title('Avg ROI by Platform × Duration', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Platform', fontsize=12)
ax.set_ylabel('Average ROI', fontsize=12)
ax.legend(title='Duration', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts/11_platform_duration_roi.png')
plt.close()
print("✅ Chart 11 saved — Platform × Duration ROI")

# ─────────────────────────────────────────
# ADVANCED 2: Platform × Segment
# Which segment performs best on which platform?
# ─────────────────────────────────────────
print("\n📊 ADVANCED 2: Platform × Customer Segment (Avg ROI)")
plat_seg = df.groupby(['Channel_Used', 'Customer_Segment'])['ROI'].mean().round(2).unstack()
print(plat_seg.to_string())

# Chart — Heatmap
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(plat_seg, annot=True, fmt='.2f', cmap='RdYlGn',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Avg ROI'})
ax.set_title('Platform × Customer Segment — Average ROI', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Customer Segment', fontsize=11)
ax.set_ylabel('Platform', fontsize=11)
plt.tight_layout()
plt.savefig('charts/12_platform_segment_heatmap.png')
plt.close()
print("✅ Chart 12 saved — Platform × Segment Heatmap")

# ─────────────────────────────────────────
# ADVANCED 3: Platform × Location
# Which city gives best ROI per platform?
# ─────────────────────────────────────────
print("\n📊 ADVANCED 3: Platform × Location (Avg ROI)")
plat_loc = df.groupby(['Channel_Used', 'Location'])['ROI'].mean().round(2).unstack()
print(plat_loc.to_string())

# Chart
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(plat_loc, annot=True, fmt='.2f', cmap='RdYlGn',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Avg ROI'})
ax.set_title('Platform × Location — Average ROI', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Location', fontsize=11)
ax.set_ylabel('Platform', fontsize=11)
plt.tight_layout()
plt.savefig('charts/13_platform_location_heatmap.png')
plt.close()
print("✅ Chart 13 saved — Platform × Location Heatmap")

# ─────────────────────────────────────────
# ADVANCED 4: Cost Efficiency Ranking
# Rank platforms by cost efficiency tiers
# ─────────────────────────────────────────
print("\n📊 ADVANCED 4: Cost Efficiency Analysis by Platform")
cost_eff = df.groupby('Channel_Used').agg(
    Avg_CPC              = ('CPC', 'mean'),
    Avg_CPM              = ('CPM', 'mean'),
    Avg_ROI              = ('ROI', 'mean'),
    Avg_Acquisition_Cost = ('Acquisition_Cost', 'mean'),
    ROI_Per_Dollar_CPC   = ('ROI', lambda x: x.mean() / df.loc[x.index, 'CPC'].mean())
).round(2)
cost_eff['Efficiency_Tier'] = cost_eff['Avg_ROI'].apply(
    lambda x: '🟢 High' if x >= 3.5 else ('🟡 Medium' if x >= 2.0 else '🔴 Low')
)
print(cost_eff.to_string())

# ─────────────────────────────────────────
# ADVANCED 5: Engagement Score Deep Dive
# ─────────────────────────────────────────
print("\n📊 ADVANCED 5: Engagement Score Buckets vs ROI")
df['Engagement_Bucket'] = pd.cut(
    df['Engagement_Score'],
    bins=[0, 3, 6, 10],
    labels=['Low (1–3)', 'Medium (4–6)', 'High (7–10)']
)
eng_roi = df.groupby(['Channel_Used', 'Engagement_Bucket'], observed=True)['ROI'].mean().round(2).unstack()
print(eng_roi.to_string())

# Chart
fig, ax = plt.subplots(figsize=(9, 5))
eng_roi.plot(kind='bar', ax=ax, edgecolor='white', width=0.6,
             color=['#e74c3c', '#f39c12', '#2ecc71'])
ax.set_title('ROI by Platform × Engagement Score Bucket',
             fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Platform', fontsize=12)
ax.set_ylabel('Average ROI', fontsize=12)
ax.legend(title='Engagement Level', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts/14_engagement_bucket_roi.png')
plt.close()
print("✅ Chart 14 saved — Engagement Bucket ROI")

# ─────────────────────────────────────────
# ADVANCED 6: ROI Distribution per Platform
# Shows spread and consistency
# ─────────────────────────────────────────
print("\n📊 ADVANCED 6: ROI Distribution by Platform")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
platforms = ['Instagram', 'Facebook', 'Twitter', 'Pinterest']
colors    = ['#e91e8c', '#3b5998', '#1da1f2', '#e60023']

for ax, platform, color in zip(axes.flatten(), platforms, colors):
    data = df[df['Channel_Used'] == platform]['ROI']
    ax.hist(data, bins=40, color=color, edgecolor='white', alpha=0.85)
    ax.axvline(data.mean(), color='black', linestyle='--',
               linewidth=1.5, label=f'Mean: {data.mean():.2f}')
    ax.set_title(f'{platform} — ROI Distribution', fontweight='bold')
    ax.set_xlabel('ROI')
    ax.set_ylabel('Count')
    ax.legend(fontsize=9)

plt.suptitle('ROI Distribution by Platform', fontsize=15,
             fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('charts/15_roi_distribution.png', bbox_inches='tight')
plt.close()
print("✅ Chart 15 saved — ROI Distribution")

# ─────────────────────────────────────────
# ADVANCED 7: CPC Distribution per Platform
# ─────────────────────────────────────────
print("\n📊 ADVANCED 7: CPC Distribution by Platform")
fig, ax = plt.subplots(figsize=(10, 5))
for platform, color in zip(platforms, colors):
    data = df[df['Channel_Used'] == platform]['CPC']
    ax.hist(data, bins=40, alpha=0.55, color=color,
            edgecolor='white', label=platform)

ax.set_title('CPC Distribution by Platform', fontsize=14,
             fontweight='bold', pad=15)
ax.set_xlabel('Cost Per Click ($)', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('charts/16_cpc_distribution.png')
plt.close()
print("✅ Chart 16 saved — CPC Distribution")

# ─────────────────────────────────────────
# ADVANCED 8: Budget Reallocation Simulation
# What if we moved Pinterest budget to Instagram?
# ─────────────────────────────────────────
print("\n📊 ADVANCED 8: Budget Reallocation Simulation")

pinterest_spend   = df[df['Channel_Used'] == 'Pinterest']['Acquisition_Cost'].sum()
pinterest_revenue = df[df['Channel_Used'] == 'Pinterest']['Estimated_Revenue'].sum()
instagram_roi     = df[df['Channel_Used'] == 'Instagram']['ROI'].mean()

simulated_revenue = pinterest_spend * (1 + instagram_roi)
revenue_gain      = simulated_revenue - pinterest_revenue

print(f"\n  Pinterest actual spend        : ${pinterest_spend:,.0f}")
print(f"  Pinterest actual revenue      : ${pinterest_revenue:,.0f}")
print(f"  If reallocated to Instagram   :")
print(f"    Simulated revenue           : ${simulated_revenue:,.0f}")
print(f"    Additional revenue gained   : ${revenue_gain:,.0f}")
print(f"    That's +{(revenue_gain/pinterest_revenue)*100:.1f}% more revenue")
print(f"    from the same budget")

# ─────────────────────────────────────────
# ADVANCED 9: Top Performing Combinations
# Best Platform + Goal + Segment combos
# ─────────────────────────────────────────
print("\n📊 ADVANCED 9: Top 15 Platform + Goal + Segment Combinations (Avg ROI)")
combo = df.groupby(['Channel_Used', 'Campaign_Goal', 'Customer_Segment']).agg(
    Avg_ROI        = ('ROI', 'mean'),
    Avg_CTR        = ('CTR', 'mean'),
    Avg_Conversion = ('Conversion_Rate_Pct', 'mean'),
    Avg_CPC        = ('CPC', 'mean'),
    Count          = ('Campaign_ID', 'count')
).round(2).reset_index()

top_combos = combo.nlargest(15, 'Avg_ROI')
print(top_combos.to_string(index=False))

print("\n📊 ADVANCED 9b: Bottom 15 Combinations (Avg ROI)")
bot_combos = combo.nsmallest(15, 'Avg_ROI')
print(bot_combos.to_string(index=False))

# ─────────────────────────────────────────
# ADVANCED 10: Final Recommendation Table
# ─────────────────────────────────────────
print("\n📊 ADVANCED 10: Platform Recommendation Summary")
print("-"*60)
rec = {
    'Platform'  : ['Instagram', 'Twitter', 'Facebook', 'Pinterest'],
    'Avg_ROI'   : [4.01, 4.00, 3.99, 0.72],
    'Avg_CPC'   : [0.39, 0.39, 0.39, 0.66],
    'Verdict'   : ['✅ Scale Up', '✅ Scale Up',
                   '✅ Maintain', '🔴 Reallocate Budget'],
    'Action'    : [
        'Increase budget — highest ROI + lowest CPC',
        'Strong performer — maintain or grow',
        'Consistent returns — keep current spend',
        'Move budget to Instagram/Twitter'
    ]
}
rec_df = pd.DataFrame(rec)
print(rec_df.to_string(index=False))

print("\n✅ Week 5 Advanced Analysis Complete")
print("📁 Charts 11–16 saved to /charts folder")