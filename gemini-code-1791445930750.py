import streamlit as st
import pandas as pd
import plotly.express as px

import config
import database as db
import budget_engine as be
import recommendation_engine as re

st.set_page_config(page_title="PocketSmart AI", page_icon="💳", layout="wide")
db.init_db()

st.title("💳 PocketSmart AI — Budget & Recommendation Assistant")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Financial Settings")
    income = st.number_input("Monthly Income ($)", min_value=100.0, value=4000.0, step=100.0)
    
    st.divider()
    st.header("➕ Log Expense")
    desc = st.text_input("Description", placeholder="e.g., Grocery store run")
    category = st.selectbox("Category", config.CATEGORIES)
    amount = st.number_input("Amount ($)", min_value=0.01, value=45.0, step=5.0)
    
    if st.button("Add Expense", type="primary"):
        if desc:
            db.add_transaction(category, desc, amount)
            st.success("Logged transaction!")
            st.rerun()
        else:
            st.error("Please enter a description.")

    st.divider()
    if st.button("Reset All Transactions", type="secondary"):
        db.clear_all_data()
        st.rerun()

# Load Data
transactions_df = db.get_all_transactions()
summary = be.calculate_budget_summary(transactions_df, income)

# Metrics Banner
col1, col2, col3, col4 = st.columns(4)
col1.metric("Monthly Income", f"${summary['monthly_income']:,.2f}")
col2.metric("Total Spent", f"${summary['total_expenses']:,.2f}")
col3.metric("Remaining Budget", f"${summary['remaining_budget']:,.2f}", 
            delta=f"${summary['remaining_budget']:,.2f}", delta_color="normal" if summary['remaining_budget'] >= 0 else "inverse")
col4.metric("Savings Rate", f"{summary['savings_rate']:.1f}%")

st.divider()

# Layout: Charts & Smart Purchase Evaluator
tab1, tab2, tab3 = st.tabs(["📊 Spending Dashboard", "🤖 AI Financial Coach", "🛒 Smart Purchase Assistant"])

with tab1:
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("Category Breakdown")
        if not transactions_df.empty and summary["total_expenses"] > 0:
            fig = px.pie(
                values=list(summary["category_breakdown"].values()),
                names=list(summary["category_breakdown"].keys()),
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expenses logged yet. Add one in the sidebar!")

    with col_b:
        st.subheader("Recent Transactions")
        if not transactions_df.empty:
            st.dataframe(transactions_df[["date", "description", "category", "amount"]], hide_index=True, use_container_width=True)
        else:
            st.write("No transaction records.")

with tab2:
    st.subheader("🤖 AI Budget Analysis & Optimization")
    if st.button("Generate AI Financial Plan"):
        if not config.GEMINI_API_KEY:
            st.error("Missing `GEMINI_API_KEY` in `.env`.")
        else:
            with st.spinner("Analyzing spending patterns..."):
                recent_txs = transactions_df.to_dict("records") if not transactions_df.empty else []
                insights = re.get_budget_insights(summary, recent_txs)
                st.markdown(insights)

with tab3:
    st.subheader("🛒 Evaluate Planned Purchase")
    st.caption("Ask PocketSmart if a purchase fits your budget before buying.")
    
    item = st.text_input("Item Name", placeholder="e.g., Wireless Noise-Canceling Headphones")
    cost = st.number_input("Item Cost ($)", min_value=1.0, value=150.0, step=10.0)
    
    if st.button("Evaluate Purchase"):
        if not config.GEMINI_API_KEY:
            st.error("Missing `GEMINI_API_KEY` in `.env`.")
        elif item:
            with st.spinner("Evaluating budget impact..."):
                result = re.get_smart_purchase_advice(item, cost, summary)
                
                rec = result.get("recommendation", "PASS")
                if rec == "BUY":
                    st.success(f" Verdict: **{rec}**")
                elif rec == "WAIT":
                    st.warning(f" Verdict: **{rec}**")
                else:
                    st.error(f" Verdict: **{rec}**")
                    
                st.write(f"**Impact:** {result.get('impact_analysis')}")
                st.info(f"💡 **Suggestion:** {result.get('alternative_suggestion')}")