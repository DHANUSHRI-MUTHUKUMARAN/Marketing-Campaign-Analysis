import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Marketing Campaign Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #2d3250);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #3d4466;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #4fc3f7;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #9ea3b0;
        margin-top: 4px;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e0e0e0;
        border-left: 4px solid #4fc3f7;
        padding-left: 10px;
        margin: 20px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, parse_dates=['Date'])
    if 'CTR' not in df.columns:
        df['CTR'] = (df['Clicks'] / df['Impressions']) * 100
    if 'Conversion_Rate_Pct' not in df.columns:
        df['Conversion_Rate_Pct'] = df['Conversion_Rate'] * 100
    if 'CPC' not in df.columns:
        df['CPC'] = df['Acquisition_Cost'] / df['Clicks']
    if 'CPM' not in df.columns:
        df['CPM'] = (df['Acquisition_Cost'] / df['Impressions']) * 1000
    if 'Estimated_Revenue' not in df.columns:
        df['Estimated_Revenue'] = df['Acquisition_Cost'] * (1 + df['ROI'])
    if 'Month_Name' not in df.columns:
        df['Month_Name'] = df['Date'].dt.strftime('%B')
    if 'Quarter' not in df.columns:
        df['Quarter'] = df['Date'].dt.quarter
    if 'Duration_Days' not in df.columns:
        df['Duration_Days'] = df['Duration'].str.extract(r'(\d+)').astype(int)
    return df

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/combo-chart.png", width=60)
    st.title("📊 Campaign Analyzer")
    st.markdown("---")

    uploaded_file = st.file_uploader("Upload Dataset (CSV)", type=["csv"])

    if uploaded_file:
        df_raw = load_data(uploaded_file)

        st.markdown("### 🔍 Filters")

        platforms = st.multiselect(
            "Platform",
            options=sorted(df_raw['Channel_Used'].unique()),
            default=sorted(df_raw['Channel_Used'].unique())
        )
        goals = st.multiselect(
            "Campaign Goal",
            options=sorted(df_raw['Campaign_Goal'].unique()),
            default=sorted(df_raw['Campaign_Goal'].unique())
        )
        segments = st.multiselect(
            "Customer Segment",
            options=sorted(df_raw['Customer_Segment'].unique()),
            default=sorted(df_raw['Customer_Segment'].unique())
        )
        locations = st.multiselect(
            "Location",
            options=sorted(df_raw['Location'].unique()),
            default=sorted(df_raw['Location'].unique())
        )
        durations = st.multiselect(
            "Duration",
            options=sorted(df_raw['Duration'].unique()),
            default=sorted(df_raw['Duration'].unique())
        )

        st.markdown("---")
        st.caption(f"Total Records: {len(df_raw):,}")

# ── Main Content ──────────────────────────────────────────────────────────────
st.title("📊 Marketing Campaign Analysis Dashboard")
st.markdown("**Multi-platform performance analysis | 2022 Full Year**")

if not uploaded_file:
    st.info("👈 Upload your **processed_dataset.csv** from the sidebar to begin.")
    st.markdown("""
    ### What this dashboard shows:
    - Platform ROI and CTR comparison
    - Budget reallocation simulation
    - Campaign goal and segment performance
    - Monthly and quarterly trends
    - Top and bottom performing campaigns
    - Correlation and cost efficiency analysis
    """)
    st.stop()

# Apply filters
df = df_raw[
    (df_raw['Channel_Used'].isin(platforms)) &
    (df_raw['Campaign_Goal'].isin(goals)) &
    (df_raw['Customer_Segment'].isin(segments)) &
    (df_raw['Location'].isin(locations)) &
    (df_raw['Duration'].isin(durations))
].copy()

if df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# ─────────────────────────────────────────
# SECTION 1: KPI Cards
# ─────────────────────────────────────────
st.markdown('<div class="section-header">📌 Key Performance Indicators</div>',
            unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Total Campaigns", f"{len(df):,}")
with k2:
    st.metric("Avg ROI", f"{df['ROI'].mean():.2f}")
with k3:
    st.metric("Avg CTR", f"{df['CTR'].mean():.2f}%")
with k4:
    st.metric("Avg CPC", f"${df['CPC'].mean():.2f}")
with k5:
    total_rev = df['Estimated_Revenue'].sum()
    st.metric("Total Revenue", f"${total_rev/1e9:.2f}B")

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 2: Platform Comparison
# ─────────────────────────────────────────
st.markdown('<div class="section-header">🏆 Platform Performance</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    platform_roi = df.groupby('Channel_Used')['ROI'].mean().reset_index()
    platform_roi.columns = ['Platform', 'Avg ROI']
    platform_roi = platform_roi.sort_values('Avg ROI', ascending=False)
    color_map = {
        'Instagram': '#e91e8c', 'Facebook': '#3b5998',
        'Twitter': '#1da1f2',   'Pinterest': '#e60023'
    }
    fig1 = px.bar(platform_roi, x='Platform', y='Avg ROI',
                  color='Platform', color_discrete_map=color_map,
                  title='Average ROI by Platform',
                  text='Avg ROI')
    fig1.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig1.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    platform_ctr = df.groupby('Channel_Used')['CTR'].mean().reset_index()
    platform_ctr.columns = ['Platform', 'Avg CTR']
    platform_ctr = platform_ctr.sort_values('Avg CTR', ascending=False)
    fig2 = px.bar(platform_ctr, x='Platform', y='Avg CTR',
                  color='Platform', color_discrete_map=color_map,
                  title='Average CTR (%) by Platform',
                  text='Avg CTR')
    fig2.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig2.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig2, use_container_width=True)

# Spend vs Revenue
st.markdown('<div class="section-header">💰 Spend vs Revenue by Platform</div>',
            unsafe_allow_html=True)

rev_spend = df.groupby('Channel_Used').agg(
    Total_Spend   = ('Acquisition_Cost', 'sum'),
    Total_Revenue = ('Estimated_Revenue', 'sum')
).reset_index()
rev_spend[['Total_Spend', 'Total_Revenue']] /= 1e9

fig3 = go.Figure()
fig3.add_trace(go.Bar(name='Total Spend ($B)',
    x=rev_spend['Channel_Used'], y=rev_spend['Total_Spend'],
    marker_color='#e67e22',
    text=[f'${v:.2f}B' for v in rev_spend['Total_Spend']],
    textposition='outside'))
fig3.add_trace(go.Bar(name='Total Revenue ($B)',
    x=rev_spend['Channel_Used'], y=rev_spend['Total_Revenue'],
    marker_color='#2ecc71',
    text=[f'${v:.2f}B' for v in rev_spend['Total_Revenue']],
    textposition='outside'))
fig3.update_layout(barmode='group',
    title='Total Spend vs Revenue by Platform',
    height=400)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 3: Campaign Analysis
# ─────────────────────────────────────────
st.markdown('<div class="section-header">🎯 Campaign Goal & Segment Analysis</div>',
            unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    goal_roi = df.groupby('Campaign_Goal')['ROI'].mean().reset_index()
    goal_roi.columns = ['Campaign Goal', 'Avg ROI']
    goal_roi = goal_roi.sort_values('Avg ROI', ascending=True)
    fig4 = px.bar(goal_roi, x='Avg ROI', y='Campaign Goal',
                  orientation='h',
                  title='Avg ROI by Campaign Goal',
                  color='Avg ROI',
                  color_continuous_scale='RdYlGn',
                  text='Avg ROI')
    fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig4.update_layout(height=380, coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    seg_conv = df.groupby('Customer_Segment')['Conversion_Rate_Pct'].mean().reset_index()
    seg_conv.columns = ['Segment', 'Avg Conversion Rate (%)']
    seg_conv = seg_conv.sort_values('Avg Conversion Rate (%)', ascending=True)
    fig5 = px.bar(seg_conv, x='Avg Conversion Rate (%)', y='Segment',
                  orientation='h',
                  title='Avg Conversion Rate by Customer Segment',
                  color='Avg Conversion Rate (%)',
                  color_continuous_scale='Blues',
                  text='Avg Conversion Rate (%)')
    fig5.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig5.update_layout(height=380, coloraxis_showscale=False)
    st.plotly_chart(fig5, use_container_width=True)

# Goal × Platform Heatmap
st.markdown('<div class="section-header">🔥 Campaign Goal × Platform Heatmap</div>',
            unsafe_allow_html=True)

goal_plat = df.groupby(['Channel_Used', 'Campaign_Goal'])['ROI'].mean().round(2).unstack()
fig6 = px.imshow(goal_plat,
    text_auto=True,
    color_continuous_scale='RdYlGn',
    title='Average ROI — Campaign Goal × Platform',
    aspect='auto')
fig6.update_layout(height=350)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 4: Time Trends
# ─────────────────────────────────────────
st.markdown('<div class="section-header">📅 Time Trends</div>',
            unsafe_allow_html=True)

month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
monthly = df.groupby('Month_Name').agg(
    Avg_ROI    = ('ROI', 'mean'),
    Avg_CTR    = ('CTR', 'mean'),
    Campaigns  = ('Campaign_ID', 'count')
).reindex([m for m in month_order if m in df['Month_Name'].unique()]).reset_index()

metric_choice = st.selectbox(
    "Select metric for monthly trend:",
    ['Avg_ROI', 'Avg_CTR', 'Campaigns']
)

fig7 = px.line(monthly, x='Month_Name', y=metric_choice,
               markers=True,
               title=f'Monthly {metric_choice} Trend',
               color_discrete_sequence=['#4fc3f7'])
fig7.update_traces(line_width=2.5, marker_size=8)
fig7.update_layout(height=380)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 5: Cost Efficiency
# ─────────────────────────────────────────
st.markdown('<div class="section-header">💡 Cost Efficiency Analysis</div>',
            unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    sample = df.sample(n=min(5000, len(df)), random_state=42)
    fig8 = px.scatter(sample, x='CPC', y='ROI',
                      color='Channel_Used',
                      color_discrete_map=color_map,
                      title='CPC vs ROI by Platform (Sample)',
                      opacity=0.4,
                      size_max=6)
    fig8.update_layout(height=400)
    st.plotly_chart(fig8, use_container_width=True)

with col6:
    dur_perf = df.groupby('Duration').agg(
        Avg_CTR = ('CTR', 'mean'),
        Avg_ROI = ('ROI', 'mean')
    ).reset_index()
    fig9 = go.Figure()
    fig9.add_trace(go.Scatter(
        x=dur_perf['Duration'], y=dur_perf['Avg_CTR'],
        name='Avg CTR (%)', mode='lines+markers',
        line=dict(color='#3498db', width=2.5),
        marker=dict(size=8)))
    fig9.add_trace(go.Scatter(
        x=dur_perf['Duration'], y=dur_perf['Avg_ROI'],
        name='Avg ROI', mode='lines+markers',
        line=dict(color='#e74c3c', width=2.5, dash='dash'),
        marker=dict(size=8),
        yaxis='y2'))
    fig9.update_layout(
        title='Duration vs CTR and ROI',
        yaxis=dict(title='Avg CTR (%)', color='#3498db'),
        yaxis2=dict(title='Avg ROI', color='#e74c3c',
                    overlaying='y', side='right'),
        height=400)
    st.plotly_chart(fig9, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 6: Budget Reallocation Simulator
# ─────────────────────────────────────────
st.markdown('<div class="section-header">🔁 Budget Reallocation Simulator</div>',
            unsafe_allow_html=True)

if 'Pinterest' in platforms:
    pinterest_spend   = df[df['Channel_Used'] == 'Pinterest']['Acquisition_Cost'].sum()
    pinterest_revenue = df[df['Channel_Used'] == 'Pinterest']['Estimated_Revenue'].sum()

    target_platform = st.selectbox(
        "Reallocate Pinterest budget to:",
        [p for p in ['Instagram', 'Twitter', 'Facebook'] if p in platforms]
    )

    if target_platform:
        target_roi     = df[df['Channel_Used'] == target_platform]['ROI'].mean()
        sim_revenue    = pinterest_spend * (1 + target_roi)
        revenue_gain   = sim_revenue - pinterest_revenue
        pct_gain       = (revenue_gain / pinterest_revenue) * 100

        r1, r2, r3 = st.columns(3)
        r1.metric("Pinterest Budget", f"${pinterest_spend/1e6:.1f}M")
        r2.metric("Pinterest Revenue", f"${pinterest_revenue/1e9:.2f}B")
        r3.metric(f"If Moved to {target_platform}",
                  f"${sim_revenue/1e9:.2f}B",
                  delta=f"+${revenue_gain/1e9:.2f}B (+{pct_gain:.1f}%)")

        fig10 = go.Figure(go.Bar(
            x=['Pinterest (Current)', f'{target_platform} (Simulated)'],
            y=[pinterest_revenue/1e9, sim_revenue/1e9],
            marker_color=['#e60023', '#2ecc71'],
            text=[f'${pinterest_revenue/1e9:.2f}B', f'${sim_revenue/1e9:.2f}B'],
            textposition='outside'
        ))
        fig10.update_layout(
            title=f'Revenue Impact: Pinterest → {target_platform}',
            yaxis_title='Revenue (Billions $)',
            height=380
        )
        st.plotly_chart(fig10, use_container_width=True)
else:
    st.info("Include Pinterest in your platform filter to use the reallocation simulator.")

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 7: Top & Bottom Campaigns
# ─────────────────────────────────────────
st.markdown('<div class="section-header">🏅 Top & Bottom Campaigns</div>',
            unsafe_allow_html=True)

n = st.slider("Number of campaigns to show", 5, 20, 10)
col7, col8 = st.columns(2)

cols_show = ['Campaign_ID', 'Channel_Used', 'Campaign_Goal',
             'Customer_Segment', 'Location', 'Duration',
             'ROI', 'CTR', 'CPC']

with col7:
    st.markdown("**🟢 Top Campaigns by ROI**")
    st.dataframe(
        df.nlargest(n, 'ROI')[cols_show].round(2).reset_index(drop=True),
        use_container_width=True
    )

with col8:
    st.markdown("**🔴 Bottom Campaigns by ROI**")
    st.dataframe(
        df.nsmallest(n, 'ROI')[cols_show].round(2).reset_index(drop=True),
        use_container_width=True
    )

st.markdown("---")

# ─────────────────────────────────────────
# SECTION 8: Recommendations
# ─────────────────────────────────────────
st.markdown('<div class="section-header">📋 Final Recommendations</div>',
            unsafe_allow_html=True)

st.markdown("""
| # | Recommendation | Action |
|---|---|---|
| 1 | 🔴 Stop spending on Pinterest | ROI = 0.72 vs 4.00 on all other platforms |
| 2 | ✅ Scale up Instagram & Twitter | Highest ROI + lowest CPC ($0.39) |
| 3 | 💡 Optimize CPC below $0.45 | CPC > $0.57 → ROI collapses to 0.81 |
| 4 | 📈 Monitor engagement early | Engagement score predicts ROI (r = 0.35) |
| 5 | ⏱️ Default to 30-day campaigns | Best CTR/ROI balance |
""")

st.markdown("---")
st.caption("Marketing Campaign Analysis Dashboard | Built with Streamlit & Plotly")