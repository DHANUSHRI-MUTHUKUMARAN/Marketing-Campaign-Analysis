import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

df = pd.read_csv("processed_dataset.csv", parse_dates=['Date'])
os.makedirs("charts", exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 150

print("="*60)
print("MARKETING CAMPAIGN ANALYSIS — WEEK 6 INSIGHTS REPORT")
print("="*60)

# ─────────────────────────────────────────
# INSIGHT 1: The Pinterest Problem
# ─────────────────────────────────────────
print("\n" + "="*60)
print("INSIGHT 1: THE PINTEREST PROBLEM")
print("="*60)

platform_summary = df.groupby('Channel_Used').agg(
    Total_Spend      = ('Acquisition_Cost', 'sum'),
    Total_Revenue    = ('Estimated_Revenue', 'sum'),
    Avg_ROI          = ('ROI', 'mean'),
    Avg_CPC          = ('CPC', 'mean'),
    ROI_Per_CPC_Dollar = ('ROI', lambda x: round(
        x.mean() / df.loc[x.index, 'CPC'].mean(), 2))
).round(2)
platform_summary['Revenue_Per_Dollar_Spent'] = (
    platform_summary['Total_Revenue'] /
    platform_summary['Total_Spend']
).round(2)
platform_summary['Verdict'] = platform_summary['Avg_ROI'].apply(
    lambda x: '✅ SCALE UP' if x >= 3.5 else '🔴 REALLOCATE'
)

print(platform_summary[[
    'Avg_ROI', 'Avg_CPC', 'Revenue_Per_Dollar_Spent',
    'ROI_Per_CPC_Dollar', 'Verdict'
]].sort_values('Avg_ROI', ascending=False).to_string())

# Chart — ROI vs CPC Bubble Chart
platform_stats = df.groupby('Channel_Used').agg(
    Avg_ROI = ('ROI', 'mean'),
    Avg_CPC = ('CPC', 'mean'),
    Count   = ('Campaign_ID', 'count')
).reset_index()

fig, ax = plt.subplots(figsize=(9, 6))
colors = {'Instagram': '#e91e8c', 'Facebook': '#3b5998',
          'Twitter': '#1da1f2', 'Pinterest': '#e60023'}
for _, row in platform_stats.iterrows():
    ax.scatter(row['Avg_CPC'], row['Avg_ROI'],
               s=row['Count'] / 20,
               color=colors[row['Channel_Used']],
               alpha=0.85, edgecolors='white', linewidth=1.5)
    ax.annotate(row['Channel_Used'],
                (row['Avg_CPC'], row['Avg_ROI']),
                textcoords='offset points',
                xytext=(10, 5), fontsize=11, fontweight='bold',
                color=colors[row['Channel_Used']])

ax.axhline(y=3.5, color='gray', linestyle='--',
           linewidth=1.2, label='ROI threshold (3.5)')
ax.set_title('Platform Positioning: CPC vs ROI\n(Bubble size = Campaign Count)',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Average CPC ($)', fontsize=12)
ax.set_ylabel('Average ROI', fontsize=12)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('charts/17_platform_positioning.png')
plt.close()
print("\n✅ Chart 17 saved — Platform Positioning Bubble Chart")

# ─────────────────────────────────────────
# INSIGHT 2: CPC Is the ROI Driver
# ─────────────────────────────────────────
print("\n" + "="*60)
print("INSIGHT 2: CPC IS THE PRIMARY ROI DRIVER")
print("="*60)

# CPC Quartile Analysis
df['CPC_Quartile'] = pd.qcut(df['CPC'], q=4,
    labels=['Q1 Lowest', 'Q2 Low-Mid', 'Q3 Mid-High', 'Q4 Highest'])
cpc_analysis = df.groupby('CPC_Quartile', observed=True).agg(
    CPC_Range  = ('CPC', lambda x: f"${x.min():.2f}–${x.max():.2f}"),
    Avg_ROI    = ('ROI', 'mean'),
    Avg_CTR    = ('CTR', 'mean'),
    Count      = ('Campaign_ID', 'count')
).round(2)
print(cpc_analysis.to_string())

# Chart
cpc_roi = df.groupby('CPC_Quartile', observed=True)['ROI'].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
bar_colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
bars = ax.bar(cpc_roi['CPC_Quartile'], cpc_roi['ROI'],
              color=bar_colors, edgecolor='white', width=0.5)
ax.bar_label(bars, fmt='%.2f', padding=4,
             fontsize=11, fontweight='bold')
ax.set_title('Average ROI by CPC Quartile\n(Lower CPC = Higher ROI)',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('CPC Quartile', fontsize=12)
ax.set_ylabel('Average ROI', fontsize=12)
ax.set_ylim(0, cpc_roi['ROI'].max() * 1.2)
plt.tight_layout()
plt.savefig('charts/18_cpc_quartile_roi.png')
plt.close()
print("\n✅ Chart 18 saved — CPC Quartile vs ROI")

# ─────────────────────────────────────────
# INSIGHT 3: Engagement Predicts ROI
# ─────────────────────────────────────────
print("\n" + "="*60)
print("INSIGHT 3: ENGAGEMENT SCORE PREDICTS ROI (Moderately)")
print("="*60)

eng_analysis = df.groupby('Engagement_Score').agg(
    Avg_ROI = ('ROI', 'mean'),
    Avg_CTR = ('CTR', 'mean'),
    Count   = ('Campaign_ID', 'count')
).round(2)
print(eng_analysis.to_string())

# Chart
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(eng_analysis.index, eng_analysis['Avg_ROI'],
        'o-', color='#9b59b6', linewidth=2.5, markersize=8)
ax.fill_between(eng_analysis.index, eng_analysis['Avg_ROI'],
                alpha=0.15, color='#9b59b6')
for score, row in eng_analysis.iterrows():
    ax.annotate(f"{row['Avg_ROI']:.2f}",
                (score, row['Avg_ROI']),
                textcoords='offset points',
                xytext=(0, 8), ha='center', fontsize=9)
ax.set_title('Engagement Score vs Average ROI',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Engagement Score (1–10)', fontsize=12)
ax.set_ylabel('Average ROI', fontsize=12)
ax.set_xticks(range(1, 11))
plt.tight_layout()
plt.savefig('charts/19_engagement_vs_roi.png')
plt.close()
print("\n✅ Chart 19 saved — Engagement Score vs ROI")

# ─────────────────────────────────────────
# INSIGHT 4: Budget Reallocation Impact
# ─────────────────────────────────────────
print("\n" + "="*60)
print("INSIGHT 4: BUDGET REALLOCATION SIMULATION")
print("="*60)

pinterest_spend   = df[df['Channel_Used'] == 'Pinterest']['Acquisition_Cost'].sum()
pinterest_revenue = df[df['Channel_Used'] == 'Pinterest']['Estimated_Revenue'].sum()
instagram_roi     = df[df['Channel_Used'] == 'Instagram']['ROI'].mean()
twitter_roi       = df[df['Channel_Used'] == 'Twitter']['ROI'].mean()

sim_instagram = pinterest_spend * (1 + instagram_roi)
sim_twitter   = pinterest_spend * (1 + twitter_roi)
gain_instagram = sim_instagram - pinterest_revenue
gain_twitter   = sim_twitter   - pinterest_revenue

print(f"\n  Pinterest Budget              : ${pinterest_spend:,.0f}")
print(f"  Pinterest Actual Revenue      : ${pinterest_revenue:,.0f}")
print(f"\n  Scenario A → Move to Instagram")
print(f"    Projected Revenue           : ${sim_instagram:,.0f}")
print(f"    Revenue Gain                : +${gain_instagram:,.0f} (+{gain_instagram/pinterest_revenue*100:.1f}%)")
print(f"\n  Scenario B → Move to Twitter")
print(f"    Projected Revenue           : ${sim_twitter:,.0f}")
print(f"    Revenue Gain                : +${gain_twitter:,.0f} (+{gain_twitter/pinterest_revenue*100:.1f}%)")

# Chart — Before vs After
labels   = ['Pinterest\n(Current)', 'Instagram\n(Simulated)', 'Twitter\n(Simulated)']
revenues = [pinterest_revenue/1e9, sim_instagram/1e9, sim_twitter/1e9]
bar_cols  = ['#e60023', '#e91e8c', '#1da1f2']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, revenues, color=bar_cols,
              edgecolor='white', width=0.45)
ax.bar_label(bars, fmt='$%.2fB', padding=4,
             fontsize=11, fontweight='bold')
ax.set_title('Budget Reallocation: Revenue Impact\n(Same $583M Budget)',
             fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Projected Revenue (Billions $)', fontsize=12)
ax.set_ylim(0, max(revenues) * 1.2)
ax.axhline(y=pinterest_revenue/1e9, color='gray',
           linestyle='--', linewidth=1.2,
           label=f'Pinterest baseline (${pinterest_revenue/1e9:.2f}B)')
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('charts/20_reallocation_impact.png')
plt.close()
print("\n✅ Chart 20 saved — Budget Reallocation Impact")

# ─────────────────────────────────────────
# FINAL REPORT: Written Recommendations
# ─────────────────────────────────────────
print("\n" + "="*60)
print("FINAL RECOMMENDATIONS REPORT")
print("="*60)

report = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MARKETING CAMPAIGN ANALYSIS — FINAL RECOMMENDATIONS
Dataset: 300,000 campaigns | 4 Platforms | Full Year 2022
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDATION 1: STOP SPENDING ON PINTEREST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Problem  : Pinterest ROI = 0.72 vs 4.00 on all other platforms
  Evidence : Same $583M budget → Pinterest: $1.0B revenue
             Same $583M budget → Instagram: $2.9B revenue
  Action   : Reallocate Pinterest budget immediately
  Impact   : +$1.92B additional revenue (+191.8%)

RECOMMENDATION 2: PRIORITIZE INSTAGRAM & TWITTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Instagram: ROI 4.01 | CPC $0.39 | Rev/$ = $5.01
  Twitter  : ROI 4.00 | CPC $0.39 | Rev/$ = $5.00
  Action   : Increase budget allocation to these two platforms
  Best combos:
    → Instagram + Increase Sales + Fashion    (ROI: 4.08)
    → Instagram + Brand Awareness + Fashion   (ROI: 4.06)
    → Twitter   + Product Launch + Technology (ROI: 4.06)

RECOMMENDATION 3: OPTIMIZE CPC TO MAXIMIZE ROI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Evidence : CPC vs ROI correlation = -0.53 (strong negative)
  Finding  : Lowest CPC quartile ($0.24–$0.35) → highest ROI
  Action   : Set CPC bid caps, use automated bidding strategies
             to keep CPC below $0.45 across all campaigns

RECOMMENDATION 4: USE ENGAGEMENT SCORE AS EARLY SIGNAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Evidence : Engagement score correlates with ROI (r = 0.35)
  Action   : Monitor engagement in first 7 days of campaign
             Scale up budget for high-engagement campaigns early
             Pause low-engagement campaigns before full spend

RECOMMENDATION 5: DURATION STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Finding  : 30-day campaigns offer best CTR/ROI balance
             60-day campaigns gain CTR but not extra ROI
  Action   : Default to 30-day campaigns
             Use 15-day campaigns for time-sensitive promotions
             Avoid 60-day campaigns unless brand awareness goal

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY: Platform > Segment > Location > Duration
         CPC optimization is the #1 controllable lever
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
print(report)

print("✅ Week 6 Insights & Recommendations Complete")
print("📁 Charts 17–20 saved to /charts folder")
print("\n🎯 PROJECT STATUS: Analysis 100% Complete")
print("   Next → Week 7: Streamlit Dashboard (Optional)")
print("   Next → Week 8: Documentation & Presentation")