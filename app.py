import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import io
import re
from datetime import datetime
   
# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Finance Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e, #16213e);
        border: 1px solid #2a3550;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 4px;
    }
    .metric-value { font-size: 28px; font-weight: 700; color: #00ff88; }
    .metric-label { font-size: 12px; color: #8892a4; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
    .insight-box {
        background: linear-gradient(135deg, #0d2137, #0a1628);
        border-left: 3px solid #00ff88;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.7;
    }
    .warning-box {
        background: linear-gradient(135deg, #2a1a0e, #1a1208);
        border-left: 3px solid #ff9f43;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 8px 0;
    }
    .category-chip {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        margin: 2px;
    }
    h1 { color: #ffffff !important; }
    .stButton > button {
        background: linear-gradient(135deg, #00ff88, #00cc6a);
        color: #0e1117;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 10px 28px;
        font-size: 15px;
        width: 100%;
    }
    .stButton > button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ── Category definitions ──────────────────────────────────────────────────────
CATEGORIES = {
    "Food & Dining":    ["restaurant", "cafe", "coffee", "pizza", "burger", "sushi", "mcdonald", "starbucks", "subway", "kfc", "food", "dining", "eat", "lunch", "dinner", "breakfast", "grubhub", "doordash", "ubereats", "zomato", "swiggy"],
    "Transport":        ["uber", "lyft", "taxi", "metro", "bus", "train", "gas", "petrol", "fuel", "parking", "toll", "ola", "rapido", "transit"],
    "Shopping":         ["amazon", "flipkart", "walmart", "target", "ebay", "shop", "store", "mall", "market", "purchase", "order", "myntra", "ajio", "meesho"],
    "Entertainment":    ["netflix", "spotify", "youtube", "prime", "hulu", "disney", "cinema", "movie", "game", "steam", "playstation", "xbox", "hotstar", "zee5"],
    "Health":           ["pharmacy", "doctor", "hospital", "clinic", "medicine", "gym", "fitness", "yoga", "health", "medical", "dental"],
    "Utilities":        ["electricity", "water", "gas bill", "internet", "wifi", "phone", "mobile", "broadband", "bill", "recharge", "airtel", "jio", "bsnl"],
    "Groceries":        ["grocery", "supermarket", "bigbasket", "blinkit", "zepto", "instamart", "dmart", "reliance fresh", "more supermarket", "vegetables", "fruits"],
    "Education":        ["udemy", "coursera", "college", "school", "tuition", "book", "course", "class", "fee", "subscription"],
    "Travel":           ["hotel", "flight", "airbnb", "booking", "makemytrip", "goibibo", "irctc", "trip", "vacation", "holiday"],
    "Transfers":        ["transfer", "sent", "received", "payment", "upi", "neft", "imps", "rtgs", "gpay", "phonepe", "paytm"],
    "Other":            [],
}

CATEGORY_COLORS = {
    "Food & Dining":    "#ff6b6b",
    "Transport":        "#ffd93d",
    "Shopping":         "#a29bfe",
    "Entertainment":    "#fd79a8",
    "Health":           "#00cec9",
    "Utilities":        "#74b9ff",
    "Groceries":        "#55efc4",
    "Education":        "#fdcb6e",
    "Travel":           "#e17055",
    "Transfers":        "#b2bec3",
    "Other":            "#636e72",
}

# ── Helper functions ──────────────────────────────────────────────────────────
def categorize_transaction(description: str) -> str:
    desc = str(description).lower()
    for category, keywords in CATEGORIES.items():
        if category == "Other":
            continue
        if any(kw in desc for kw in keywords):
            return category
    return "Other"

def parse_amount(val) -> float:
    """Parse amount from various formats: ₹1,200.50 / -1200 / 1,200.50"""
    try:
        cleaned = re.sub(r"[₹$€£,\s]", "", str(val))
        return abs(float(cleaned))
    except Exception:
        return 0.0

def detect_columns(df: pd.DataFrame):
    """Auto-detect date, description, amount columns."""
    cols = [c.lower() for c in df.columns]
    date_col  = next((df.columns[i] for i, c in enumerate(cols) if any(k in c for k in ["date", "time", "day"])), None)
    desc_col  = next((df.columns[i] for i, c in enumerate(cols) if any(k in c for k in ["desc", "narr", "detail", "particular", "remark", "note", "merchant", "name"])), None)
    amt_col   = next((df.columns[i] for i, c in enumerate(cols) if any(k in c for k in ["amount", "debit", "credit", "amt", "value", "sum", "withdrawal"])), None)
    return date_col, desc_col, amt_col

def format_currency(amount: float) -> str:
    if amount >= 1_00_000:
        return f"₹{amount/1_00_000:.1f}L"
    elif amount >= 1_000:
        return f"₹{amount/1_000:.1f}K"
    return f"₹{amount:,.0f}"

def get_ai_advice(df: pd.DataFrame, category_totals: dict, total_spent: float, api_key: str) -> str:
    """Call Gemini API for personalised financial advice."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        top_cats = sorted(category_totals.items(), key=lambda x: -x[1])[:6]
        breakdown = "\n".join([f"  - {cat}: ₹{amt:,.0f} ({amt/total_spent*100:.1f}%)" for cat, amt in top_cats])
        num_txns  = len(df)
        avg_txn   = total_spent / max(num_txns, 1)

        prompt = f"""You are a friendly, smart personal finance advisor. Analyse this spending data and give actionable advice.

SPENDING SUMMARY:
- Total transactions: {num_txns}
- Total spent: ₹{total_spent:,.0f}
- Average transaction: ₹{avg_txn:,.0f}

BREAKDOWN BY CATEGORY:
{breakdown}

Please provide:
1. **Overall Assessment** — Is this spending pattern healthy? (2-3 sentences)
2. **Top 3 Concerns** — What spending areas are worrying and why?
3. **Top 3 Money-Saving Tips** — Specific, actionable tips based on the actual data above
4. **Smart Budgeting Rule** — Suggest a realistic monthly budget split using the 50/30/20 rule adapted to this person's data
5. **One Positive** — Something they're doing right

Keep the tone friendly, encouraging, and practical. Use Indian Rupee context. Format with clear headers and bullet points."""

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Could not fetch AI advice: {str(e)}\n\nTip: Make sure your Gemini API key is correct. Get a free key at https://aistudio.google.com"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 AI Finance Advisor")
    st.markdown("---")

    st.markdown("### 🔑 Gemini API Key")
    api_key = st.text_input(
        "Enter your free Gemini API key",
        type="password",
        placeholder="AIza...",
        help="Get a FREE key at https://aistudio.google.com — no credit card needed!"
    )
    if not api_key:
        st.info("🆓 Get a FREE Gemini API key at [aistudio.google.com](https://aistudio.google.com) — no credit card required!")

    st.markdown("---")
    st.markdown("### 📋 Supported CSV Formats")
    st.markdown("""
Your CSV should have columns like:
- **Date** — transaction date
- **Description** / Narration — what it was
- **Amount** / Debit — how much

Works with exports from most banks and apps (GPay, PhonePe, Paytm, etc.)
    """)

    st.markdown("---")
    st.markdown("### 🔒 Privacy")
    st.markdown("All processing happens **locally on your machine**. Your data is never stored.")

    st.markdown("---")
    st.markdown("### 📥 Try a Sample")
    if st.button("Load Sample Data"):
        st.session_state["use_sample"] = True

# ── Sample data ───────────────────────────────────────────────────────────────
def get_sample_data() -> pd.DataFrame:
    data = {
        "Date": [
            "2024-01-02","2024-01-03","2024-01-04","2024-01-05","2024-01-06",
            "2024-01-07","2024-01-08","2024-01-10","2024-01-11","2024-01-12",
            "2024-01-13","2024-01-14","2024-01-15","2024-01-16","2024-01-17",
            "2024-01-18","2024-01-19","2024-01-20","2024-01-22","2024-01-23",
            "2024-01-24","2024-01-25","2024-01-26","2024-01-28","2024-01-29",
            "2024-01-30","2024-01-31","2024-02-01","2024-02-02","2024-02-03",
        ],
        "Description": [
            "Swiggy Food Order","Uber Ride to Office","Amazon Shopping","Netflix Subscription","BigBasket Grocery",
            "Starbucks Coffee","Airtel Mobile Recharge","Zomato Dinner","Ola Cab","Spotify Premium",
            "DMart Grocery","Doctor Consultation","Udemy Course","Restaurant Dinner","Metro Card Recharge",
            "Amazon Prime Annual","Electricity Bill","Uber Eats Lunch","PhonePe Transfer","Gym Membership",
            "BookMyShow Movie","Reliance Fresh Vegetables","MakeMyTrip Flight","Cafe Coffee Day","Petrol Fill",
            "Water Bill","Flipkart Purchase","Swiggy Instamart","Gas Bill","Zomato Brunch",
        ],
        "Amount": [
            450, 280, 2400, 649, 1850,
            320, 399, 680, 190, 119,
            2100, 500, 999, 1200, 200,
            1499, 1800, 350, 5000, 2000,
            380, 450, 8500, 180, 1200,
            350, 3200, 550, 800, 520,
        ],
    }
    return pd.DataFrame(data)

# ── Main UI ───────────────────────────────────────────────────────────────────
st.markdown("# 💰 AI Personal Finance Advisor")
st.markdown("##### Upload your bank/UPI statement CSV → Get instant AI-powered spending insights")
st.markdown("---")

# File upload or sample
df_raw = None
use_sample = st.session_state.get("use_sample", False)

if use_sample:
    df_raw = get_sample_data()
    st.success("✅ Sample data loaded! Scroll down to see your analysis.")
    if st.button("Clear & Upload My Own CSV"):
        st.session_state["use_sample"] = False
        st.rerun()
else:
    uploaded = st.file_uploader(
        "📂 Drop your CSV here (bank statement, UPI export, expense sheet)",
        type=["csv"],
        help="Supports most bank CSV exports and UPI app statements"
    )
    if uploaded:
        try:
            df_raw = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Could not read file: {e}")

# ── Process data ──────────────────────────────────────────────────────────────
if df_raw is not None:
    df = df_raw.copy()

    # Auto-detect or let user map columns
    date_col, desc_col, amt_col = detect_columns(df)

    if not all([date_col, desc_col, amt_col]):
        st.warning("⚠️ Could not auto-detect columns. Please map them manually:")
        col1, col2, col3 = st.columns(3)
        with col1:
            date_col = st.selectbox("📅 Date column", df.columns)
        with col2:
            desc_col = st.selectbox("📝 Description column", df.columns)
        with col3:
            amt_col  = st.selectbox("💵 Amount column", df.columns)

    # Parse and clean
    df["_date"]   = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
    df["_desc"]   = df[desc_col].astype(str)
    df["_amount"] = df[amt_col].apply(parse_amount)
    df["_category"] = df["_desc"].apply(categorize_transaction)
    df = df[df["_amount"] > 0].dropna(subset=["_date"])
    df = df.sort_values("_date")

    if df.empty:
        st.error("No valid transactions found. Please check your CSV format.")
        st.stop()

    # ── KPI Metrics ───────────────────────────────────────────────────────────
    total_spent   = df["_amount"].sum()
    avg_per_day   = total_spent / max(df["_date"].nunique(), 1)
    num_txns      = len(df)
    top_category  = df.groupby("_category")["_amount"].sum().idxmax()
    biggest_txn   = df.loc[df["_amount"].idxmax()]

    st.markdown("## 📊 Your Spending Overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{format_currency(total_spent)}</div><div class="metric-label">Total Spent</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{num_txns}</div><div class="metric-label">Transactions</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{format_currency(avg_per_day)}</div><div class="metric-label">Avg Per Day</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{top_category.split()[0]}</div><div class="metric-label">Top Category</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    category_totals = df.groupby("_category")["_amount"].sum().sort_values(ascending=False).to_dict()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### 🥧 Spending by Category")
        pie_df = pd.DataFrame(list(category_totals.items()), columns=["Category", "Amount"])
        fig_pie = px.pie(
            pie_df, values="Amount", names="Category",
            color="Category",
            color_discrete_map=CATEGORY_COLORS,
            hole=0.45,
        )
        fig_pie.update_traces(textposition="outside", textinfo="percent+label", textfont_size=11)
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=360,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.markdown("### 📈 Daily Spending Trend")
        daily = df.groupby("_date")["_amount"].sum().reset_index()
        daily.columns = ["Date", "Amount"]
        daily["7d_avg"] = daily["Amount"].rolling(7, min_periods=1).mean()
        fig_line = go.Figure()
        fig_line.add_trace(go.Bar(x=daily["Date"], y=daily["Amount"], name="Daily", marker_color="#2a3550", opacity=0.8))
        fig_line.add_trace(go.Scatter(x=daily["Date"], y=daily["7d_avg"], name="7-day avg", line=dict(color="#00ff88", width=2.5)))
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis=dict(gridcolor="#1a2a3a", showgrid=True),
            yaxis=dict(gridcolor="#1a2a3a", showgrid=True),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=10, b=10, l=10, r=10),
            height=360,
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # ── Category bar chart ────────────────────────────────────────────────────
    st.markdown("### 💸 Category Breakdown")
    bar_df = pd.DataFrame(list(category_totals.items()), columns=["Category", "Amount"])
    bar_df["Percentage"] = (bar_df["Amount"] / total_spent * 100).round(1)
    bar_df["Color"] = bar_df["Category"].map(CATEGORY_COLORS)
    fig_bar = px.bar(
        bar_df.sort_values("Amount"), x="Amount", y="Category",
        orientation="h",
        color="Category",
        color_discrete_map=CATEGORY_COLORS,
        text=bar_df.sort_values("Amount")["Percentage"].astype(str) + "%",
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        showlegend=False,
        xaxis=dict(gridcolor="#1a2a3a"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        margin=dict(t=10, b=10, l=10, r=10),
        height=380,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── Transaction table ─────────────────────────────────────────────────────
    st.markdown("### 🧾 All Transactions")
    filter_cat = st.multiselect(
        "Filter by category",
        options=list(category_totals.keys()),
        default=list(category_totals.keys()),
    )
    filtered_df = df[df["_category"].isin(filter_cat)][["_date", "_desc", "_amount", "_category"]].copy()
    filtered_df.columns = ["Date", "Description", "Amount (₹)", "Category"]
    filtered_df["Date"] = filtered_df["Date"].dt.strftime("%d %b %Y")
    filtered_df["Amount (₹)"] = filtered_df["Amount (₹)"].map(lambda x: f"₹{x:,.0f}")
    st.dataframe(filtered_df, use_container_width=True, height=280)

    # ── AI Advice ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🤖 AI Financial Advice")

    if not api_key:
        st.markdown("""
<div class="warning-box">
⚠️ <b>Add your free Gemini API key in the sidebar to unlock AI advice!</b><br/>
Get one free at <a href="https://aistudio.google.com" target="_blank">aistudio.google.com</a> — no credit card needed.
</div>
        """, unsafe_allow_html=True)
    else:
        if st.button("🤖 Analyse My Spending & Get AI Advice"):
            with st.spinner("🧠 AI is analysing your spending patterns..."):
                advice = get_ai_advice(df, category_totals, total_spent, api_key)
            st.markdown(f'<div class="insight-box">{advice}</div>', unsafe_allow_html=True)

    # ── Quick insights (no API needed) ───────────────────────────────────────
    st.markdown("### 💡 Quick Insights")
    insights = []

    # Biggest spender category
    top_cat, top_amt = list(category_totals.items())[0]
    top_pct = top_amt / total_spent * 100
    if top_pct > 30:
        insights.append(f"🚨 **{top_cat}** is your biggest expense at **{top_pct:.0f}%** of total spending (₹{top_amt:,.0f}). Consider setting a monthly cap.")

    # Food delivery check
    food_amt = category_totals.get("Food & Dining", 0)
    food_pct = food_amt / total_spent * 100
    if food_pct > 20:
        insights.append(f"🍔 You're spending **{food_pct:.0f}%** on Food & Dining (₹{food_amt:,.0f}). Cooking at home 3x a week could save ₹{food_amt*0.4:,.0f}+.")

    # Entertainment check
    ent_amt = category_totals.get("Entertainment", 0)
    if ent_amt > 2000:
        insights.append(f"🎬 Entertainment spend is ₹{ent_amt:,.0f}. Audit your subscriptions — you might be paying for services you rarely use.")

    # Transaction count
    if num_txns > 50:
        insights.append(f"📱 You made **{num_txns} transactions** — that's a lot of small purchases. Micro-spends add up fast!")

    # Biggest single transaction
    insights.append(f"💸 Your biggest single transaction was **₹{biggest_txn['_amount']:,.0f}** on **{biggest_txn['_desc']}**.")

    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

    # ── 50/30/20 Budget ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 📐 50/30/20 Budget Planner")
    st.markdown("Enter your monthly income to see your ideal budget split:")

    income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=5000)
    if income > 0:
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"""
<div class="metric-card">
  <div class="metric-value" style="color:#00ff88;">₹{income*0.5:,.0f}</div>
  <div class="metric-label">50% — Needs</div>
  <div style="font-size:11px;color:#8892a4;margin-top:8px;">Rent, groceries, utilities, transport</div>
</div>""", unsafe_allow_html=True)
        with b2:
            st.markdown(f"""
<div class="metric-card">
  <div class="metric-value" style="color:#ffd93d;">₹{income*0.3:,.0f}</div>
  <div class="metric-label">30% — Wants</div>
  <div style="font-size:11px;color:#8892a4;margin-top:8px;">Dining, entertainment, shopping</div>
</div>""", unsafe_allow_html=True)
        with b3:
            st.markdown(f"""
<div class="metric-card">
  <div class="metric-value" style="color:#ff6b6b;">₹{income*0.2:,.0f}</div>
  <div class="metric-label">20% — Savings</div>
  <div style="font-size:11px;color:#8892a4;margin-top:8px;">Emergency fund, investments, SIP</div>
</div>""", unsafe_allow_html=True)

        # Compare actual vs recommended
        if total_spent > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            needs_cats  = ["Utilities", "Groceries", "Health", "Transport"]
            wants_cats  = ["Food & Dining", "Entertainment", "Shopping", "Travel", "Education"]
            actual_needs = sum(category_totals.get(c, 0) for c in needs_cats)
            actual_wants = sum(category_totals.get(c, 0) for c in wants_cats)
            status_needs = "✅" if actual_needs <= income * 0.5 else "⚠️ Over budget"
            status_wants = "✅" if actual_wants <= income * 0.3 else "⚠️ Over budget"
            st.markdown(f"""
| Category | Recommended | Your Actual | Status |
|---|---|---|---|
| Needs | ₹{income*0.5:,.0f} | ₹{actual_needs:,.0f} | {status_needs} |
| Wants | ₹{income*0.3:,.0f} | ₹{actual_wants:,.0f} | {status_wants} |
| Savings Target | ₹{income*0.2:,.0f} | — | Set up a SIP! |
""")

else:
    # ── Landing / empty state ─────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center; padding: 60px 20px;">
  <div style="font-size: 72px;">💰</div>
  <h2 style="color:#e8eaf0;">Upload your bank statement to get started</h2>
  <p style="color:#8892a4; font-size:15px; max-width:520px; margin: 0 auto;">
    Drop any CSV file with your transactions — from your bank, Google Pay, PhonePe, Paytm, or any expense tracker.
    The AI will categorise everything and give you personalised money advice.
  </p>
  <br/>
  <p style="color:#8892a4; font-size:13px;">
    👈 Or click <b>"Load Sample Data"</b> in the sidebar to see a demo instantly.
  </p>
</div>
""", unsafe_allow_html=True)
