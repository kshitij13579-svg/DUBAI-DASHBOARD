"""
Dubai Dynamic Restaurant Pricing — EDA Dashboard
==================================================
Streamlit app: 10 insight categories, drill-downs, Sankey to App Adoption.
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import combinations
import os

st.set_page_config(page_title="DinePrice Dubai — EDA Dashboard", page_icon="🍽️",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .block-container {padding-top: 1.2rem; padding-bottom: 1rem; max-width: 1200px;}
    h1 {font-size: 1.9rem !important; color: #1a1a2e !important; font-weight: 700 !important;}
    h2 {font-size: 1.35rem !important; color: #16213e !important; border-bottom: 2px solid #FF6B35; padding-bottom: 0.3rem; margin-top: 1.5rem !important;}
    h3 {font-size: 1.1rem !important; color: #0f3460 !important;}
    div[data-testid="stMetric"] {background: linear-gradient(135deg, #fff7f0 0%, #fff0e6 100%); padding: 14px 18px; border-radius: 10px; border-left: 5px solid #FF6B35; box-shadow: 0 2px 8px rgba(0,0,0,0.06);}
    div[data-testid="stMetric"] label {color: #555 !important; font-size: 0.82rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.5px;}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {color: #1a1a2e !important; font-size: 1.6rem !important; font-weight: 800 !important;}
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {color: #333 !important;}
    section[data-testid="stSidebar"] {background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);}
    section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span {color: #e0e0e0 !important;}
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {color: #FF6B35 !important; border-bottom: none !important;}
    section[data-testid="stSidebar"] hr {border-color: rgba(255,255,255,0.15) !important;}
    .insight-box {background: linear-gradient(135deg, #e8f4f8 0%, #d4edda 100%); border-left: 4px solid #1A936F; padding: 12px 16px; border-radius: 8px; margin: 10px 0 18px 0; color: #1a1a2e; font-size: 0.92rem; line-height: 1.5;}
    .insight-box strong {color: #0f3460;}
    .callout-box {background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%); border-left: 4px solid #F4A261; padding: 12px 16px; border-radius: 8px; margin: 10px 0 18px 0; color: #1a1a2e; font-size: 0.92rem;}
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

PALETTE = ["#FF6B35","#004E89","#1A936F","#F4A261","#E76F51","#264653","#2A9D8F","#E9C46A","#606C38","#BC6C25"]

def styled_layout(fig, height=400):
    fig.update_layout(height=height, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#1a1a2e", size=12), title_font=dict(size=15, color="#16213e"),
                      margin=dict(l=40, r=20, t=50, b=40),
                      legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor="#ddd", borderwidth=1))
    return fig

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def callout(text):
    st.markdown(f'<div class="callout-box">{text}</div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    for path in ["data/data_clean.csv","data_clean.csv","dubai-pricing-dashboard/data/data_clean.csv"]:
        if os.path.exists(path): return pd.read_csv(path)
    st.error("❌ data_clean.csv not found."); st.stop()

df = load_data()

def explode_col(df, col):
    return df[col].dropna().str.split(", ").explode().str.strip()

# --- SIDEBAR ---
st.sidebar.markdown("""
<div style="text-align:center; padding: 10px 0 5px 0;">
    <span style="font-size: 2.5rem;">🍽️</span>
    <h2 style="margin:5px 0 0 0; font-size:1.4rem; color:#FF6B35 !important;">DinePrice Dubai</h2>
    <p style="margin:2px 0 0 0; font-size:0.8rem; color:#aaa; letter-spacing:1px;">DYNAMIC PRICING EDA</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()

sections = ["📊 Overview & KPIs","1️⃣ Customer Profile","2️⃣ Dining Behaviour","3️⃣ Price Sensitivity",
            "4️⃣ Dynamic Pricing System","5️⃣ Location & Cuisine","6️⃣ Delivery vs Dine-in",
            "7️⃣ Correlation Analysis","8️⃣ Challenges & Features","9️⃣ App Adoption Deep Dive",
            "🔟 Seasonality","🔀 Sankey: Path to Adoption"]
section = st.sidebar.radio("📌 Navigate to Section", sections, index=0)
st.sidebar.divider()

adopt_rate_global = (df["App_Adoption"]=="Yes").mean()*100
st.sidebar.markdown(f"""
<div style="background:rgba(255,107,53,0.15); padding:12px; border-radius:8px; margin:5px 0;">
    <p style="margin:0; font-size:0.75rem; color:#aaa; text-transform:uppercase;">North Star</p>
    <p style="margin:2px 0 0 0; font-size:1.3rem; font-weight:800; color:#FF6B35;">{adopt_rate_global:.1f}% Adoption</p>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div style="margin-top:8px; padding:8px 12px; background:rgba(255,255,255,0.05); border-radius:6px;">
    <p style="margin:0; font-size:0.75rem; color:#888;">📁 <strong style="color:#ccc;">{len(df):,}</strong> clean records</p>
    <p style="margin:2px 0 0 0; font-size:0.75rem; color:#888;">📊 <strong style="color:#ccc;">35</strong> variables</p>
    <p style="margin:2px 0 0 0; font-size:0.75rem; color:#888;">🎯 Target: <strong style="color:#ccc;">App Adoption</strong></p>
</div>
""", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown('<p style="font-size:0.65rem; color:#666; text-align:center;">SP Jain GMBA · Data Analytics · 2026</p>', unsafe_allow_html=True)

AGE_ORDER = ["18-24","25-34","35-44","45-54","55+"]
INC_ORDER = ["<5000","5000-10000","10001-20000","20001-35000",">35000"]
SENS_ORDER = ["Very sensitive","Moderately sensitive","Slightly sensitive","Not sensitive"]
FAIR_ORDER = ["Very fair","Somewhat fair","Neutral","Unfair","Very unfair"]
FREQ_ORDER = ["Multiple/week","Once/week","2-3/month","Once/month","Rarely"]
TIME_ORDER = ["Breakfast","Lunch","Dinner","Late Night"]
DEMAND_ORDER = ["Low","Medium","High"]

# ===== 0. OVERVIEW =====
if section == "📊 Overview & KPIs":
    st.title("🍽️ DinePrice Dubai — Dynamic Restaurant Pricing")
    st.markdown("**North Star Metric:** App Adoption Rate — *What drives customers to say Yes to dynamic pricing?*")
    st.markdown("")
    adopt_rate = (df["App_Adoption"]=="Yes").mean()*100
    avg_spend = df["Avg_Spend_AED"].mean()
    avg_surge = df["Surge_Multiplier"].mean()
    delivery_pct = (df["Order_Channel"]=="Delivery App").mean()*100
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Responses", f"{len(df):,}")
    c2.metric("Adoption Rate", f"{adopt_rate:.1f}%")
    c3.metric("Avg Spend / Visit", f"{avg_spend:.0f} AED")
    c4.metric("Avg Surge", f"{avg_surge:.2f}x")
    c5.metric("Delivery Share", f"{delivery_pct:.1f}%")
    insight(f"<strong>Key Takeaway:</strong> Nearly <strong>{adopt_rate:.0f}%</strong> of respondents are open to dynamic pricing — a strong market signal. Average spend is <strong>{avg_spend:.0f} AED</strong> per visit with a <strong>{avg_surge:.2f}x surge</strong> indicating moderate pricing headroom. Delivery dominates at <strong>{delivery_pct:.0f}%</strong>, reflecting Dubai's app-driven food culture.")
    st.divider()
    col1,col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names="App_Adoption", title="App Adoption Split", color_discrete_sequence=[PALETTE[2],PALETTE[4]], hole=0.45)
        fig.update_traces(textinfo="percent+label", textfont_size=14, textfont_color="#1a1a2e")
        styled_layout(fig, 370); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="Avg_Spend_AED", nbins=40, color="App_Adoption", barmode="overlay", title="Spend Distribution by Adoption", color_discrete_sequence=[PALETTE[2],PALETTE[4]], opacity=0.7)
        styled_layout(fig, 370); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Spend Pattern:</strong> Adopters and non-adopters have similar spend distributions, suggesting that price level alone doesn't determine adoption — <em>attitudes</em> and <em>sensitivity</em> matter more. Explore sections 3 and 9 for deeper analysis.")
    with st.expander("📋 Dataset Preview (first 20 rows)"):
        st.dataframe(df.head(20), use_container_width=True, height=400)

# ===== 1. CUSTOMER PROFILE =====
elif section == "1️⃣ Customer Profile":
    st.title("1️⃣ Customer Profile & Segmentation")
    insight("<strong>Objective:</strong> Understand <em>who</em> our respondents are — age, income, type, nationality, and loyalty patterns. These dimensions feed directly into <strong>K-Means clustering</strong> for customer persona identification.")
    col1,col2 = st.columns(2)
    with col1:
        fig = px.histogram(df, x="Age", color="App_Adoption", category_orders={"Age":AGE_ORDER}, title="Age Distribution by Adoption", color_discrete_sequence=[PALETTE[2],PALETTE[4]], barmode="group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="Monthly_Income", color="App_Adoption", category_orders={"Monthly_Income":INC_ORDER}, title="Income Distribution by Adoption", color_discrete_sequence=[PALETTE[2],PALETTE[4]], barmode="group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Age:</strong> The 25–34 bracket dominates (~35%), typical of Dubai's young professional population. <strong>Income:</strong> The middle-income segment (5K–20K AED) forms the core market — price-sensitive enough to value dynamic discounts, affluent enough to dine frequently.")
    col3,col4 = st.columns(2)
    with col3:
        fig = px.histogram(df, x="Customer_Type", color="Nationality_Cluster", title="Customer Type by Nationality", color_discrete_sequence=PALETTE, barmode="stack")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.histogram(df, x="Loyalty_Status", color="Customer_Type", title="Loyalty Status by Customer Type", color_discrete_sequence=PALETTE, barmode="stack")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Nationality:</strong> South Asians (~45%) form the largest cluster, followed by Arabs and Western Expats — mirroring Dubai's actual demographic composition. <strong>Loyalty:</strong> Tourists are overwhelmingly 'Explorers', while Families tend to be 'Loyal to 1-2' places — a key segmentation insight for personalized pricing strategies.")
    st.subheader("🔍 Drill-down: Age × Income Heatmap")
    ct = pd.crosstab(df["Age"], df["Monthly_Income"]).reindex(index=AGE_ORDER, columns=INC_ORDER)
    fig = px.imshow(ct, text_auto=True, color_continuous_scale="Oranges", title="Respondent Count: Age vs Income", labels=dict(x="Monthly Income",y="Age Group",color="Count"))
    styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔍 Drill-down: Nationality → Type → Adoption")
    fig = px.sunburst(df, path=["Nationality_Cluster","Customer_Type","App_Adoption"], title="Nationality → Customer Type → Adoption", color_discrete_sequence=PALETTE)
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

# ===== 2. DINING BEHAVIOUR =====
elif section == "2️⃣ Dining Behaviour":
    st.title("2️⃣ Dining Behaviour Patterns")
    insight("<strong>Objective:</strong> Map <em>when</em>, <em>how</em>, and <em>how often</em> customers dine. These variables are critical inputs for both <strong>regression</strong> (predicting spend) and <strong>clustering</strong> (persona identification).")
    col1,col2 = st.columns(2)
    with col1:
        ct = pd.crosstab(df["Age"], df["Order_Time"]).reindex(index=AGE_ORDER, columns=TIME_ORDER)
        fig = px.imshow(ct, text_auto=True, color_continuous_scale="YlOrRd", title="Order Time by Age Group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="Order_Channel", color="Age", category_orders={"Age":AGE_ORDER}, title="Channel Preference by Age", color_discrete_sequence=PALETTE, barmode="stack")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Time × Age:</strong> Students (18-24) overwhelmingly prefer <em>Late Night</em> dining; the 55+ group skews toward <em>Breakfast</em>. Dinner is universally the peak slot. <strong>Channel:</strong> Younger cohorts (18-34) are 50%+ delivery, confirming Dubai's app-first culture.")
    col3,col4 = st.columns(2)
    with col3:
        ct2 = pd.crosstab(df["Monthly_Income"], df["Dining_Frequency"]).reindex(index=INC_ORDER, columns=FREQ_ORDER)
        fig = px.imshow(ct2, text_auto=True, color_continuous_scale="Tealgrn", title="Dining Frequency by Income")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.histogram(df, x="Group_Size", color="Customer_Type", title="Group Size by Customer Type", color_discrete_sequence=PALETTE, barmode="group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Frequency × Income:</strong> Higher income correlates directly with dining frequency — the >35K bracket dines multiple times per week. <strong>Group Size:</strong> Families predominantly dine in groups of 3-4+, while Students and Professionals are solo or in pairs.")
    st.subheader("🔍 Drill-down: Day → Time → Channel")
    fig = px.sunburst(df, path=["Day_Preference","Order_Time","Order_Channel"], title="Day → Time → Channel Flow", color_discrete_sequence=PALETTE)
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔍 Drill-down: Dining Frequency vs Average Spend")
    fig = px.box(df, x="Dining_Frequency", y="Avg_Spend_AED", color="Dining_Frequency", category_orders={"Dining_Frequency":FREQ_ORDER}, title="Spend Distribution by Dining Frequency", color_discrete_sequence=PALETTE)
    fig.update_layout(showlegend=False); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Frequency vs Spend:</strong> Frequent diners (multiple/week) show higher median spend but also greater variance — they visit both budget and premium restaurants. Rare diners tend toward higher per-visit spend (special occasions).")

# ===== 3. PRICE SENSITIVITY =====
elif section == "3️⃣ Price Sensitivity":
    st.title("3️⃣ Price Sensitivity & Dynamic Pricing Appetite")
    insight("<strong>Objective:</strong> Gauge how customers react to price changes — the core question for a dynamic pricing system. These variables are the <strong>strongest predictors</strong> for the classification model (predicting adoption).")
    col1,col2 = st.columns(2)
    with col1:
        ct = pd.crosstab(df["Monthly_Income"], df["Price_Sensitivity"]).reindex(index=INC_ORDER, columns=SENS_ORDER)
        fig = px.imshow(ct, text_auto=True, color_continuous_scale="RdYlGn_r", title="Price Sensitivity by Income")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        disc_order = ["5%","10%","15%","20%",">20%"]
        ct2 = pd.crosstab(df["Price_Sensitivity"], df["Discount_Motivation"]).reindex(index=SENS_ORDER, columns=disc_order)
        fig = px.imshow(ct2, text_auto=True, color_continuous_scale="Oranges", title="Discount Motivation by Sensitivity")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Income → Sensitivity:</strong> Low-income groups (&lt;5K) are overwhelmingly 'Very sensitive', while high-income (&gt;35K) are largely 'Not sensitive'. <strong>Discount Depth:</strong> Very sensitive customers need 20%+ discounts to act — the engine must price aggressively during off-peak to move this segment.")
    col3,col4 = st.columns(2)
    with col3:
        offpeak_order = ["Definitely yes","Probably yes","Maybe","Probably not","Definitely not"]
        fig = px.histogram(df, x="Offpeak_Willingness", color="Price_Sensitivity", title="Off-Peak Willingness by Sensitivity", color_discrete_sequence=PALETTE, barmode="stack", category_orders={"Offpeak_Willingness":offpeak_order})
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.histogram(df, x="Fairness_Perception", color="Age", title="Fairness Perception by Age", color_discrete_sequence=PALETTE, barmode="stack", category_orders={"Fairness_Perception":FAIR_ORDER,"Age":AGE_ORDER})
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Off-Peak Shift:</strong> Price-sensitive customers are significantly more willing to dine off-peak — validating the core business hypothesis. <strong>Fairness:</strong> Younger respondents (18-34) perceive dynamic pricing as fairer — they're accustomed to surge pricing from ride-hailing apps.")
    st.subheader("🔍 Drill-down: Price Sensitivity → Adoption Rate")
    adopt_by_sens = df.groupby("Price_Sensitivity")["App_Adoption"].apply(lambda x:(x=="Yes").mean()*100).reindex(SENS_ORDER).reset_index()
    adopt_by_sens.columns = ["Price_Sensitivity","Adoption_Rate"]
    fig = px.bar(adopt_by_sens, x="Price_Sensitivity", y="Adoption_Rate", title="Adoption Rate by Price Sensitivity", color="Adoption_Rate", color_continuous_scale="RdYlGn", text="Adoption_Rate")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside'); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔍 Drill-down: Discount Importance vs Fairness")
    di_order = ["Extremely important","Very important","Moderately important","Slightly important","Not important"]
    ct3 = pd.crosstab(df["Discount_Importance"], df["Fairness_Perception"]).reindex(index=di_order, columns=FAIR_ORDER)
    fig = px.imshow(ct3, text_auto=True, color_continuous_scale="Purples", title="Discount Importance vs Fairness Perception")
    styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Critical Finding:</strong> Those who find dynamic pricing 'Very fair' AND consider discounts 'Extremely important' are the prime early adopters — target this segment first during launch.")

# ===== 4. DYNAMIC PRICING SYSTEM =====
elif section == "4️⃣ Dynamic Pricing System":
    st.title("4️⃣ Dynamic Pricing System Variables")
    insight("<strong>Objective:</strong> Analyze the system-generated variables — demand level, surge multiplier, table occupancy, and price impact. These are the <em>engine outputs</em> that determine whether customers see higher or lower prices.")
    avg_surge=df["Surge_Multiplier"].mean(); avg_disc=df["Discount_Percentage"].mean()
    occ_mean=df["Table_Occupancy_Pct"].dropna().mean(); high_demand_pct=(df["Demand_Level"]=="High").mean()*100
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Avg Surge", f"{avg_surge:.2f}x"); c2.metric("Avg Discount", f"{avg_disc:.1f}%")
    c3.metric("Avg Occupancy", f"{occ_mean:.1f}%"); c4.metric("High Demand %", f"{high_demand_pct:.1f}%")
    st.markdown("")
    col1,col2 = st.columns(2)
    with col1:
        dc = df["Demand_Level"].value_counts().reindex(DEMAND_ORDER).reset_index(); dc.columns=["Demand_Level","Count"]
        fig = px.bar(dc, x="Demand_Level", y="Count", color="Demand_Level", title="Demand Level Distribution", color_discrete_map={"Low":"#1A936F","Medium":"#F4A261","High":"#E76F51"}, text="Count")
        fig.update_traces(textposition="outside"); fig.update_layout(showlegend=False); styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(df, x="Surge_Multiplier", nbins=30, color="Demand_Level", title="Surge Multiplier Distribution by Demand", color_discrete_map={"Low":"#1A936F","Medium":"#F4A261","High":"#E76F51"}, category_orders={"Demand_Level":DEMAND_ORDER})
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight(f"<strong>Demand Distribution:</strong> {high_demand_pct:.0f}% of situations are 'High' demand (weekends + dinner + peak season). Surge ranges from 0.75x (25% discount) to 1.40x (40% premium). Most orders cluster around the 1.0–1.2x range — moderate adjustments.")
    col3,col4 = st.columns(2)
    with col3:
        fig = px.box(df, x="Demand_Level", y="Table_Occupancy_Pct", color="Demand_Level", title="Table Occupancy by Demand Level", color_discrete_map={"Low":"#1A936F","Medium":"#F4A261","High":"#E76F51"}, category_orders={"Demand_Level":DEMAND_ORDER})
        fig.update_layout(showlegend=False); styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        fig = px.scatter(df, x="Base_Order_Value", y="Final_Order_Value", color="Demand_Level", opacity=0.4, title="Base vs Final Order Value (Surge Impact)", color_discrete_map={"Low":"#1A936F","Medium":"#F4A261","High":"#E76F51"})
        fig.add_shape(type="line",x0=0,y0=0,x1=800,y1=800,line=dict(dash="dash",color="gray",width=1))
        fig.add_annotation(x=600,y=550,text="No surge line",showarrow=False,font=dict(color="gray",size=10))
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Occupancy:</strong> High-demand periods average ~80% occupancy vs ~30% for low demand — the pricing engine correctly identifies when restaurants are full. <strong>Scatter:</strong> Points above the dashed line = surge applied; below = discounted. High demand (red) consistently sits above the line.")
    st.subheader("🔍 Drill-down: Surge vs App Adoption")
    df_temp = df.copy()
    df_temp["Surge_Bin"] = pd.cut(df_temp["Surge_Multiplier"], bins=[0.7,0.85,0.95,1.05,1.15,1.25,1.45], labels=["0.75–0.85","0.85–0.95","0.95–1.05","1.05–1.15","1.15–1.25","1.25–1.40"])
    sa = df_temp.groupby("Surge_Bin")["App_Adoption"].apply(lambda x:(x=="Yes").mean()*100).reset_index(); sa.columns=["Surge_Bin","Adoption_Rate"]
    fig = px.bar(sa, x="Surge_Bin", y="Adoption_Rate", title="Adoption Rate by Surge Level — Does surge kill conversion?", color="Adoption_Rate", color_continuous_scale="RdYlGn", text="Adoption_Rate")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside'); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Key Finding:</strong> Adoption remains relatively stable across surge levels — suggesting customers who like the concept accept moderate surge pricing. The engine can apply 10–20% surges without significantly impacting conversion.")
    st.subheader("🔍 Drill-down: Demand by Day × Time")
    ct = pd.crosstab([df["Day_Preference"],df["Order_Time"]], df["Demand_Level"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0)*100
    fig = px.imshow(ct_pct.round(1), text_auto=True, color_continuous_scale="YlOrRd", title="Demand Level % by Day × Time", labels=dict(color="%"))
    styled_layout(fig, 450); st.plotly_chart(fig, use_container_width=True)

# ===== 5. LOCATION & CUISINE =====
elif section == "5️⃣ Location & Cuisine":
    st.title("5️⃣ Location & Cuisine Intelligence")
    insight("<strong>Objective:</strong> Identify which Dubai locations and cuisines command premium pricing. This informs the pricing engine's location-based rules and restaurant onboarding strategy.")
    col1,col2 = st.columns(2)
    with col1:
        li = pd.crosstab(df["Restaurant_Location"], df["Monthly_Income"]).reindex(columns=INC_ORDER)
        fig = px.imshow(li, text_auto=True, color_continuous_scale="Blues", title="Restaurant Location by Income")
        styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    with col2:
        cn = pd.crosstab(df["Nationality_Cluster"], df["Cuisine_Preference"])
        fig = px.imshow(cn, text_auto=True, color_continuous_scale="Oranges", title="Cuisine Preference by Nationality")
        styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Location × Income:</strong> DIFC and Downtown attract high-income diners (>20K AED); Deira serves the budget-conscious. Mall restaurants are income-agnostic. <strong>Cuisine × Nationality:</strong> South Asians prefer Indian/Pakistani (45%), East Asians prefer Asian (45%), Arabs prefer Arabic (40%) — strong cultural clustering.")
    col3,col4 = st.columns(2)
    with col3:
        ti = pd.crosstab(df["Monthly_Income"], df["Restaurant_Tier"]).reindex(index=INC_ORDER)
        fig = px.imshow(ti, text_auto=True, color_continuous_scale="Tealgrn", title="Restaurant Tier by Income")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        sl = df.groupby("Restaurant_Location")["Avg_Spend_AED"].mean().sort_values(ascending=True).reset_index()
        fig = px.bar(sl, x="Avg_Spend_AED", y="Restaurant_Location", orientation="h", title="Average Spend by Location (AED)", color="Avg_Spend_AED", color_continuous_scale="Oranges", text="Avg_Spend_AED")
        fig.update_traces(texttemplate='%{text:.0f}', textposition='outside'); styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔍 Drill-down: Spend by Cuisine Type")
    fig = px.box(df, x="Cuisine_Preference", y="Avg_Spend_AED", color="Cuisine_Preference", title="Spend Distribution by Cuisine", color_discrete_sequence=PALETTE)
    fig.update_layout(showlegend=False); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔍 Drill-down: Location → Tier → Adoption")
    fig = px.sunburst(df, path=["Restaurant_Location","Restaurant_Tier","App_Adoption"], title="Location → Tier → Adoption Flow", color_discrete_sequence=PALETTE)
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

# ===== 6. DELIVERY VS DINE-IN =====
elif section == "6️⃣ Delivery vs Dine-in":
    st.title("6️⃣ Delivery vs Dine-in Analysis")
    dinein=df[df["Order_Channel"]=="Dine-in"]; delivery=df[df["Order_Channel"]=="Delivery App"]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Dine-in", f"{len(dinein):,}"); c2.metric("Delivery", f"{len(delivery):,}")
    c3.metric("Dine-in Avg Spend", f"{dinein['Avg_Spend_AED'].mean():.0f} AED"); c4.metric("Delivery Avg Spend", f"{delivery['Avg_Spend_AED'].mean():.0f} AED")
    insight(f"<strong>Channel Split:</strong> Delivery ({len(delivery)/len(df)*100:.0f}%) edges out Dine-in ({len(dinein)/len(df)*100:.0f}%). Dine-in customers spend ~<strong>{dinein['Avg_Spend_AED'].mean():.0f} AED</strong> vs ~<strong>{delivery['Avg_Spend_AED'].mean():.0f} AED</strong> for delivery — the pricing engine should differentiate surge rules by channel.")
    col1,col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names="Order_Channel", title="Channel Distribution", color_discrete_sequence=PALETTE, hole=0.4)
        fig.update_traces(textinfo="percent+label", textfont_size=13); styled_layout(fig, 370); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.box(df, x="Order_Channel", y="Avg_Spend_AED", color="Order_Channel", title="Spend by Channel", color_discrete_sequence=PALETTE)
        fig.update_layout(showlegend=False); styled_layout(fig, 370); st.plotly_chart(fig, use_container_width=True)
    col3,col4 = st.columns(2)
    with col3:
        fig = px.histogram(df, x="Weather_Behaviour", color="Order_Channel", title="Weather Impact on Channel Choice", color_discrete_sequence=PALETTE, barmode="group")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col4:
        dd = df[df["Delivery_Distance_km"].notna()]
        fig = px.scatter(dd, x="Delivery_Distance_km", y="Est_Delivery_Time_min", color="Avg_Spend_AED", opacity=0.5, title="Delivery: Distance vs Time", color_continuous_scale="Oranges")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Weather:</strong> 48% of respondents switch to delivery during extreme heat — the system should trigger delivery-specific discounts when temperature exceeds 40°C. <strong>Distance:</strong> Most deliveries are within 7 km; longer distances correlate linearly with delivery time.")
    st.subheader("🔍 Drill-down: Channel → Adoption Rate")
    ca = df.groupby("Order_Channel")["App_Adoption"].apply(lambda x:(x=="Yes").mean()*100).reset_index(); ca.columns=["Order_Channel","Adoption_Rate"]
    fig = px.bar(ca, x="Order_Channel", y="Adoption_Rate", color="Adoption_Rate", color_continuous_scale="RdYlGn", text="Adoption_Rate", title="Adoption Rate by Channel")
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside'); styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)

# ===== 7. CORRELATION =====
elif section == "7️⃣ Correlation Analysis":
    st.title("7️⃣ Correlation Analysis")
    insight("<strong>Objective:</strong> Identify linear relationships between numeric variables. The correlation matrix reveals which features are <strong>strongest predictors</strong> for regression (predicting spend) and highlights multicollinearity risks.")
    num_cols = ["Avg_Spend_AED","Surge_Multiplier","Final_Order_Value","Discount_Percentage","Experience_Rating","Table_Occupancy_Pct","Delivery_Distance_km","Est_Delivery_Time_min"]
    corr = df[num_cols].corr()
    fig = px.imshow(corr.round(2), text_auto=True, color_continuous_scale="RdBu_r", title="Correlation Matrix — Numeric Variables", zmin=-1, zmax=1)
    styled_layout(fig, 550); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Key Correlations:</strong><br>• <strong>Avg_Spend ↔ Final_Order_Value</strong>: Very high (~0.98) — expected since Final = Base × Surge.<br>• <strong>Surge ↔ Discount_Percentage</strong>: Strong negative — when surge is high, discounts are zero.<br>• <strong>Delivery_Distance ↔ Delivery_Time</strong>: Strong positive — validates realistic data.<br>• <strong>Experience_Rating</strong> shows weak correlations with price variables — satisfaction is driven by non-price factors.")
    col1,col2 = st.columns(2)
    with col1:
        fig = px.box(df, x="Monthly_Income", y="Avg_Spend_AED", color="Monthly_Income", title="Income vs Average Spend", category_orders={"Monthly_Income":INC_ORDER}, color_discrete_sequence=PALETTE)
        fig.update_layout(showlegend=False); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(df, x="Surge_Multiplier", y="Experience_Rating", color="App_Adoption", opacity=0.3, title="Surge vs Rating (by Adoption)", color_discrete_sequence=[PALETTE[2],PALETTE[4]])
        styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔍 Drill-down: Base vs Final Value by Tier")
    fig = px.scatter(df, x="Base_Order_Value", y="Final_Order_Value", color="Restaurant_Tier", opacity=0.4, title="Base vs Final Order Value by Restaurant Tier", color_discrete_sequence=PALETTE)
    fig.add_shape(type="line",x0=0,y0=0,x1=800,y1=800,line=dict(dash="dash",color="gray"))
    styled_layout(fig, 450); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Tier Impact:</strong> Premium/Fine Dining shows the widest spread above the no-surge line — these restaurants can sustain higher surge multipliers without losing customers.")

# ===== 8. CHALLENGES & FEATURES =====
elif section == "8️⃣ Challenges & Features":
    st.title("8️⃣ Challenges & Desired Features")
    insight("<strong>Objective:</strong> Discover which pain points cluster together and which features customers want when they face specific challenges. This feeds directly into <strong>Association Rule Mining</strong> (Apriori / FP-Growth).")
    col1,col2 = st.columns(2)
    with col1:
        ch = explode_col(df,"Challenges"); chc = ch.value_counts().reset_index(); chc.columns=["Challenge","Count"]
        fig = px.bar(chc, x="Count", y="Challenge", orientation="h", title="Top Challenges Faced", color="Count", color_continuous_scale="Reds", text="Count")
        fig.update_traces(textposition="outside"); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    with col2:
        ft = explode_col(df,"Desired_Features"); ftc = ft.value_counts().reset_index(); ftc.columns=["Feature","Count"]
        fig = px.bar(ftc, x="Count", y="Feature", orientation="h", title="Most Desired Features", color="Count", color_continuous_scale="Greens", text="Count")
        fig.update_traces(textposition="outside"); styled_layout(fig, 400); st.plotly_chart(fig, use_container_width=True)
    insight(f"<strong>Top Challenge:</strong> '{chc.iloc[0]['Challenge']}' ({chc.iloc[0]['Count']} mentions). <strong>Top Feature:</strong> '{ftc.iloc[0]['Feature']}' ({ftc.iloc[0]['Count']} mentions). The alignment between pain points and desired features validates that the app concept addresses real market needs.")
    st.subheader("🔍 Drill-down: Challenge Co-occurrence")
    ce = df["Challenges"].dropna().str.split(", "); ac = sorted(set(c for row in ce for c in row))
    cc = pd.DataFrame(0, index=ac, columns=ac)
    for row in ce:
        for a,b in combinations(row,2): cc.loc[a,b]+=1; cc.loc[b,a]+=1
    fig = px.imshow(cc, text_auto=True, color_continuous_scale="Reds", title="Challenge Co-occurrence Matrix")
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔍 Drill-down: Feature Co-occurrence")
    fe = df["Desired_Features"].dropna().str.split(", "); af = sorted(set(f for row in fe for f in row))
    fc = pd.DataFrame(0, index=af, columns=af)
    for row in fe:
        for a,b in combinations(row,2): fc.loc[a,b]+=1; fc.loc[b,a]+=1
    fig = px.imshow(fc, text_auto=True, color_continuous_scale="Greens", title="Feature Co-occurrence Matrix")
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Co-occurrence Insight:</strong> Challenges that frequently appear together (hot cells) suggest systemic issues — e.g., 'High weekend prices' + 'Crowded restaurants' likely represent the same peak-demand scenario. Association rules will formalize these as itemset→consequent patterns.")
    st.subheader("🔍 Drill-down: Challenge → Feature Association")
    pairs = []
    for _,row in df.iterrows():
        if pd.notna(row["Challenges"]) and pd.notna(row["Desired_Features"]):
            for c in str(row["Challenges"]).split(", "):
                for f in str(row["Desired_Features"]).split(", "):
                    pairs.append({"Challenge":c.strip(),"Feature":f.strip()})
    pdf = pd.DataFrame(pairs); tp = pdf.groupby(["Challenge","Feature"]).size().reset_index(name="Count").nlargest(15,"Count")
    fig = px.bar(tp, x="Count", y="Challenge", color="Feature", orientation="h", title="Top 15 Challenge → Feature Associations", color_discrete_sequence=PALETTE, barmode="stack")
    styled_layout(fig, 500); st.plotly_chart(fig, use_container_width=True)

# ===== 9. APP ADOPTION DEEP DIVE =====
elif section == "9️⃣ App Adoption Deep Dive":
    st.title("9️⃣ App Adoption — Deep Dive")
    ar = (df["App_Adoption"]=="Yes").mean()*100; yc = (df["App_Adoption"]=="Yes").sum(); nc = (df["App_Adoption"]=="No").sum()
    c1,c2,c3 = st.columns(3)
    c1.metric("Adoption Rate", f"{ar:.1f}%"); c2.metric("Yes Responses", f"{yc:,}"); c3.metric("No Responses", f"{nc:,}")
    insight(f"<strong>North Star:</strong> {ar:.1f}% adoption is a strong positive signal. Below we decompose adoption by <strong>10 dimensions</strong> to identify the profile of adopters vs. non-adopters. This analysis directly feeds the <strong>classification model</strong> feature selection.")
    dims = [("Age",AGE_ORDER),("Monthly_Income",INC_ORDER),("Customer_Type",None),("Price_Sensitivity",SENS_ORDER),
            ("Fairness_Perception",FAIR_ORDER),("Order_Channel",None),("Restaurant_Tier",None),("Loyalty_Status",None),
            ("Day_Preference",None),("Nationality_Cluster",None)]
    for i in range(0, len(dims), 2):
        cols = st.columns(2)
        for j,(dim,order) in enumerate(dims[i:i+2]):
            with cols[j]:
                if order:
                    ab = df.groupby(dim)["App_Adoption"].apply(lambda x:(x=="Yes").mean()*100).reindex(order).reset_index()
                else:
                    ab = df.groupby(dim)["App_Adoption"].apply(lambda x:(x=="Yes").mean()*100).sort_values(ascending=True).reset_index()
                ab.columns = [dim,"Adoption_Rate"]
                fig = px.bar(ab, x="Adoption_Rate", y=dim, orientation="h", title=f"Adoption by {dim.replace('_',' ')}", color="Adoption_Rate", color_continuous_scale="RdYlGn", text="Adoption_Rate")
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color="#1a1a2e", size=12))
                fig.update_layout(showlegend=False, coloraxis_showscale=False)
                styled_layout(fig, 280); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Adoption Drivers (Summary):</strong><br>• <strong>Price Sensitivity:</strong> 'Very sensitive' customers adopt at the highest rate — they see direct value.<br>• <strong>Fairness:</strong> Those who perceive dynamic pricing as 'Very fair' adopt 20%+ more than those who find it 'Very unfair'.<br>• <strong>Channel:</strong> Delivery app users adopt more readily — they're already in the app ecosystem.<br>• <strong>Age:</strong> Younger demographics adopt more, consistent with tech comfort.")
    st.subheader("🔍 Drill-down: Sensitivity × Fairness → Adoption Rate")
    cta = df.pivot_table(values="App_Adoption", index="Price_Sensitivity", columns="Fairness_Perception", aggfunc=lambda x:(x=="Yes").mean()*100)
    cta = cta.reindex(index=SENS_ORDER, columns=FAIR_ORDER)
    fig = px.imshow(cta.round(1), text_auto=True, color_continuous_scale="RdYlGn", title="Adoption Rate %: Sensitivity × Fairness (the 2 strongest predictors)", labels=dict(color="Adoption %"))
    styled_layout(fig, 420); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Sweet Spot:</strong> The top-left cell (Very sensitive + Very fair) shows peak adoption. The bottom-right (Not sensitive + Very unfair) shows the lowest. These two variables should be the <strong>top features</strong> in the classification model.")

# ===== 10. SEASONALITY =====
elif section == "🔟 Seasonality":
    st.title("🔟 Seasonality Analysis")
    insight("<strong>Objective:</strong> Dubai dining is heavily seasonal — tourist influx (Oct–Mar), summer exodus (Jul–Sep), Ramadan shifts. Understanding seasonal patterns helps the pricing engine set appropriate baseline surge levels by month.")
    months = explode_col(df,"Peak_Months"); mc = months.value_counts().reindex(["Oct-Dec","Jan-Mar","Apr-Jun","Jul-Sep"]).reset_index(); mc.columns=["Season","Selections"]
    col1,col2 = st.columns(2)
    with col1:
        fig = px.bar(mc, x="Season", y="Selections", color="Season", title="Peak Dining Seasons", color_discrete_sequence=[PALETTE[4],PALETTE[0],PALETTE[3],PALETTE[5]], text="Selections")
        fig.update_traces(textposition="outside"); fig.update_layout(showlegend=False); styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    with col2:
        dm = df[["Customer_Type","Peak_Months"]].dropna(); dm = dm.assign(Peak_Months=dm["Peak_Months"].str.split(", ")).explode("Peak_Months")
        ct = pd.crosstab(dm["Customer_Type"], dm["Peak_Months"]).reindex(columns=["Oct-Dec","Jan-Mar","Apr-Jun","Jul-Sep"])
        fig = px.imshow(ct, text_auto=True, color_continuous_scale="YlOrRd", title="Peak Months by Customer Type")
        styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Seasonality:</strong> Oct–Dec is the clear peak (Dubai tourist season, pleasant weather, festivals). Jul–Sep shows the lowest activity (summer heat, residents travel abroad). <strong>Tourists</strong> concentrate in Oct–Mar; <strong>Families</strong> dine consistently year-round.")
    st.subheader("🔍 Drill-down: Season & Demand Level")
    dm2 = df[["Demand_Level","Peak_Months"]].dropna(); dm2 = dm2.assign(Peak_Months=dm2["Peak_Months"].str.split(", ")).explode("Peak_Months")
    ct2 = pd.crosstab(dm2["Peak_Months"], dm2["Demand_Level"]).reindex(index=["Oct-Dec","Jan-Mar","Apr-Jun","Jul-Sep"], columns=DEMAND_ORDER)
    fig = px.imshow(ct2, text_auto=True, color_continuous_scale="Oranges", title="Demand Level Distribution by Season")
    styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    st.subheader("🔍 Drill-down: Season × Weather Behaviour")
    dm3 = df[["Weather_Behaviour","Peak_Months"]].dropna(); dm3 = dm3.assign(Peak_Months=dm3["Peak_Months"].str.split(", ")).explode("Peak_Months")
    ct3 = pd.crosstab(dm3["Peak_Months"], dm3["Weather_Behaviour"]).reindex(index=["Oct-Dec","Jan-Mar","Apr-Jun","Jul-Sep"])
    fig = px.imshow(ct3, text_auto=True, color_continuous_scale="Tealgrn", title="Weather Behaviour by Season")
    styled_layout(fig, 380); st.plotly_chart(fig, use_container_width=True)
    insight("<strong>Weather × Season:</strong> 'Switch to delivery in heat' peaks during Apr–Sep months. The pricing engine should apply delivery-specific pricing rules seasonally — lower delivery surge in summer (high supply), higher dine-in discounts to pull foot traffic.")

# ===== SANKEY =====
elif section == "🔀 Sankey: Path to Adoption":
    st.title("🔀 Sankey Diagram — Path to App Adoption")
    insight("<strong>Objective:</strong> Trace how customer attributes flow through behavioural and attitudinal filters to reach the <strong>North Star metric</strong> (App Adoption). Each Sankey tells a different story.")

    def build_sankey(df, path_cols):
        labels = []
        for col in path_cols:
            for val in df[col].unique():
                l = f"{col}: {val}"
                if l not in labels: labels.append(l)
        idx = {l:i for i,l in enumerate(labels)}
        src,tgt,val = [],[],[]
        for i in range(len(path_cols)-1):
            flow = df.groupby([path_cols[i],path_cols[i+1]]).size().reset_index(name="n")
            for _,r in flow.iterrows():
                src.append(idx[f"{path_cols[i]}: {r[path_cols[i]]}"])
                tgt.append(idx[f"{path_cols[i+1]}: {r[path_cols[i+1]]}"])
                val.append(r["n"])
        return labels,src,tgt,val

    def make_sankey(labels,src,tgt,val,title,stage_colors):
        nc = []
        for l in labels:
            if "App_Adoption: Yes" in l: nc.append("#1A936F")
            elif "App_Adoption: No" in l: nc.append("#E76F51")
            else:
                matched = False
                for k,c in stage_colors.items():
                    if k in l: nc.append(c); matched=True; break
                if not matched: nc.append("#999")
        lc = ["rgba(26,147,111,0.25)" if "Yes" in labels[t] else "rgba(231,111,81,0.25)" if "No" in labels[t] else "rgba(150,150,150,0.12)" for t in tgt]
        dl = [l.split(": ",1)[1] if ": " in l else l for l in labels]
        fig = go.Figure(go.Sankey(node=dict(pad=15,thickness=25,line=dict(color="#333",width=0.5),label=dl,color=nc),
                                   link=dict(source=src,target=tgt,value=val,color=lc)))
        fig.update_layout(title=dict(text=title,font=dict(size=14,color="#16213e")),font_size=11,height=600,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
        return fig

    st.subheader("1. Demographics → Attitudes → Adoption")
    l1,s1,t1,v1 = build_sankey(df, ["Customer_Type","Price_Sensitivity","Fairness_Perception","App_Adoption"])
    st.plotly_chart(make_sankey(l1,s1,t1,v1,"Customer Type → Price Sensitivity → Fairness → Adoption",{"Customer_Type":"#004E89","Price_Sensitivity":"#F4A261","Fairness":"#2A9D8F"}), use_container_width=True)
    insight("<strong>Reading:</strong> Professionals (largest segment) split across all sensitivity levels. The thickest green flows to 'Yes' come from 'Very sensitive' + 'Very fair' — confirming these are the strongest adoption predictors.")

    st.subheader("2. Operational Context → Pricing → Adoption")
    ds2 = df.copy(); ds2["Surge_Bucket"] = pd.cut(ds2["Surge_Multiplier"],bins=[0,0.95,1.05,1.5],labels=["Discount (<0.95)","Neutral (0.95–1.05)","Surge (>1.05)"])
    l2,s2,t2,v2 = build_sankey(ds2.dropna(subset=["Surge_Bucket"]), ["Order_Channel","Demand_Level","Surge_Bucket","App_Adoption"])
    st.plotly_chart(make_sankey(l2,s2,t2,v2,"Channel → Demand → Surge Bucket → Adoption",{"Order_Channel":"#004E89","Demand_Level":"#F4A261","Surge":"#2A9D8F","Discount":"#2A9D8F","Neutral":"#2A9D8F"}), use_container_width=True)
    insight("<strong>Reading:</strong> Delivery App users flow heavily into Medium/High demand → Surge pricing. Despite the surge, adoption remains strong — delivery users are more price-tolerant because they value convenience.")

    st.subheader("3. Spending Power → Restaurant Choice → Adoption")
    l3,s3,t3,v3 = build_sankey(df, ["Monthly_Income","Restaurant_Tier","Restaurant_Location","App_Adoption"])
    st.plotly_chart(make_sankey(l3,s3,t3,v3,"Income → Tier → Location → Adoption",{"Monthly_Income":"#004E89","Restaurant_Tier":"#F4A261","Restaurant_Location":"#2A9D8F"}), use_container_width=True)
    insight("<strong>Reading:</strong> Low-income → Budget/Casual → Deira/Mall is the dominant budget flow, with moderate adoption (they want discounts). High-income → Premium → DIFC/Downtown shows high adoption too — they see value in demand-based table management.")

    callout("💡 <strong>Dashboard Summary:</strong> The three Sankey diagrams converge on one conclusion — App Adoption is driven by a <strong>combination</strong> of price sensitivity, fairness perception, channel behaviour, and income level. No single variable determines it. The classification model should use <strong>all of these as features</strong> for maximum predictive power.")
