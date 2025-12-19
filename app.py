import streamlit as st
import pandas as pd
import snowflake.connector

# Snowflake connection
conn = snowflake.connector.connect(
    user='YOUR_USERNAME',
    password='YOUR_PASSWORD',
    account='YOUR_ACCOUNT',
    warehouse='YOUR_WAREHOUSE',
    database='YOUR_DATABASE',
    schema='PUBLIC'
)

query = "SELECT * FROM inventory_risk_view"
df = pd.read_sql(query, conn)

st.set_page_config(page_title="Inventory Heatmap & Alerts", layout="wide")

st.title("📦 Inventory Heatmap & Stock-Out Alerts")

# Risk summary
st.subheader("🔴 Stock Risk Overview")
st.dataframe(df)

# Heatmap-style view
st.subheader("🔥 Inventory Health Status")

def color_risk(val):
    if val == "CRITICAL":
        return "background-color: #ff4d4d"
    elif val == "LOW":
        return "background-color: #ffd11a"
    else:
        return "background-color: #66ff66"

st.dataframe(df.style.applymap(color_risk, subset=["RISK_LEVEL"]))

# Alerts
st.subheader("🚨 Critical Stock Alerts")
alerts = df[df["RISK_LEVEL"] == "CRITICAL"]

if alerts.empty:
    st.success("No critical stock issues detected.")
else:
    for _, row in alerts.iterrows():
        st.error(
            f"{row['ITEM']} at {row['LOCATION']} may run out soon. "
            f"Suggested reorder: {row['SUGGESTED_REORDER_QTY']} units."
        )
