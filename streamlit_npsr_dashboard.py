# This file prepares a working Streamlit dashboard for Net Patient Service Revenue forecasting
# Upload it to GitHub and deploy via Streamlit Cloud

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# Load data
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "NPSR_Forecast_Data.csv")
df = pd.read_csv(file_path)

st.title("Strategic Forecast Dashboard: Net Patient Service Revenue (NPSR)")
st.markdown("""
This dashboard allows healthcare leaders to evaluate the financial impact of increasing visit volume vs panel size
under mixed payment models, including per-member-per-month (PMPM) capitation and fee-for-service (FFS).
""")

# Sidebar Inputs
st.sidebar.header("Model Parameters")

ffs_rate = st.sidebar.number_input("FFS Rate per Visit ($)", value=150, step=10)
pmpm_rate = st.sidebar.number_input("PMPM Rate per Member ($)", value=24, step=1)

ffs_pct = st.sidebar.slider("Percent of Patients on FFS", 0, 100, 50)
pmpm_pct = 100 - ffs_pct

panel_size = st.sidebar.slider("Panel Size (Patients)", 500, 10000, 3000, step=100)
visits_per_patient = st.sidebar.slider("Visits per Patient per Year", 1, 10, 3)

max_visits = st.sidebar.number_input("Operational Visit Capacity (Max Annual Visits)", value=10000, step=500)

# Calculations
annual_visits = panel_size * visits_per_patient
actual_visits = min(annual_visits, max_visits)

ffs_revenue = actual_visits * (ffs_pct / 100) * ffs_rate
pmpm_revenue = panel_size * (pmpm_pct / 100) * pmpm_rate * 12

total_revenue = ffs_revenue + pmpm_revenue
marginal_revenue_per_visit = ffs_rate * (ffs_pct / 100)  # Since PMPM doesn't increase with visit count

# Display
st.subheader("Revenue Forecast")
st.metric("Annual FFS Revenue", f"${ffs_revenue:,.0f}")
st.metric("Annual PMPM Revenue", f"${pmpm_revenue:,.0f}")
st.metric("Total Annual Revenue", f"${total_revenue:,.0f}")
st.metric("Marginal Revenue per Visit", f"${marginal_revenue_per_visit:,.2f}")

# Visualization
st.subheader("Revenue Breakdown")
fig, ax = plt.subplots()
revenue_sources = pd.DataFrame({
    'Type': ['FFS', 'PMPM'],
    'Revenue': [ffs_revenue, pmpm_revenue]
})
sns.barplot(data=revenue_sources, x='Type', y='Revenue', palette='Blues_d', ax=ax)
ax.set_ylabel("Annual Revenue ($)")
ax.set_title("Revenue by Payment Model")
st.pyplot(fig)
