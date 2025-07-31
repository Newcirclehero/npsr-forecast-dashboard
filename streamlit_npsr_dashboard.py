import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Revenue Strategy Comparator", layout="wide")

st.title("📊 Strategic Revenue Impact: Expand Panel vs. Increase Visits")
st.markdown("""
Use this dashboard to compare the revenue and capacity impact of:
- **Adding 1,000 patients** to your panel
- **Generating 14,000 additional visits** from existing patients

Assumes 40% of visits under PMPM generate no incremental visit revenue. Visit capacity is capped at 180,000 annually.
""")

# Sidebar Inputs
st.sidebar.header("Model Inputs")

panel_size = st.sidebar.slider("Current Panel Size", 500, 50000, 25347, step=100)
visit_rate = st.sidebar.slider("Average Visits per Patient per Year", 2.0, 5.0, 3.0, step=0.1)

ffs_pct = st.sidebar.slider("Percent of Visits that are FFS Reimbursable", 0, 100, 60, step=5)
ffs_rate = st.sidebar.slider("FFS Reimbursement per Visit ($)", 100, 300, 150, step=10)
pmpm_rate = st.sidebar.slider("PMPM Rate per Member per Month ($)", 20, 150, 25, step=5)

# Constants
visit_capacity = 180000
pmpm_pct = 100 - ffs_pct
base_visits = panel_size * visit_rate

# --- Scenario A: Add 1,000 Patients ---
added_patients = 1000
added_visits_A = added_patients * visit_rate
total_visits_A = base_visits + added_visits_A
capacity_flag_A = total_visits_A > visit_capacity

pmpm_revenue_A = added_patients * pmpm_rate * 12
ffs_revenue_A = 0  # all new patients assumed under PMPM
total_revenue_A = pmpm_revenue_A + ffs_revenue_A

# --- Scenario B: Add 14,000 Visits ---
added_visits_B = 14000
billable_visits_B = added_visits_B * (ffs_pct / 100)
total_visits_B = base_visits + added_visits_B
capacity_flag_B = total_visits_B > visit_capacity

pmpm_revenue_B = 0  # no new members added
ffs_revenue_B = billable_visits_B * ffs_rate
total_revenue_B = pmpm_revenue_B + ffs_revenue_B

# --- Output Section ---
st.subheader("📈 Scenario Comparison Table")

comparison = pd.DataFrame({
    "Scenario": ["Add 1,000 Patients", "Add 14,000 Visits"],
    "New Visits Generated": [added_visits_A, added_visits_B],
    "Total Visits After Change": [total_visits_A, total_visits_B],
    "Revenue: PMPM": [pmpm_revenue_A, pmpm_revenue_B],
    "Revenue: FFS": [ffs_revenue_A, ffs_revenue_B],
    "Total Revenue": [total_revenue_A, total_revenue_B],
    "Visit Capacity Breached": ["Yes" if capacity_flag_A else "No", "Yes" if capacity_flag_B else "No"]
})

st.dataframe(comparison.style.format({
    "Revenue: PMPM": "${:,.0f}",
    "Revenue: FFS": "${:,.0f}",
    "Total Revenue": "${:,.0f}"
}))

# --- Chart Comparison ---
st.subheader("📊 Visual Comparison")

fig, ax = plt.subplots(figsize=(8, 4))
scenarios = ["Add 1,000 Patients", "Add 14,000 Visits"]
revenues = [total_revenue_A, total_revenue_B]
colors = ["#4CAF50" if not capacity_flag_A else "#FFC107", "#4CAF50" if not capacity_flag_B else "#FFC107"]

ax.bar(scenarios, revenues, color=colors)
ax.set_ylabel("Total Revenue ($)")
ax.set_title("Total Revenue by Scenario")
st.pyplot(fig)

# --- Capacity Warnings ---
if capacity_flag_A or capacity_flag_B:
    st.warning("⚠️ One or both scenarios would exceed the annual visit capacity of 180,000 visits.")

st.markdown("This tool supports revenue modeling for primary care transformation. Built for Codman Square Health Center.")
