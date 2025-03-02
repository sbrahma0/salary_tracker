# pages/Dashboard.py
import streamlit as st
import pandas as pd
from utils.db_utils import connect_db

# Page title
st.title("Employee Salary Dashboard")
st.header("Employee Salary Overview")

# Fetch and display salary overview
conn = connect_db()
df = pd.read_sql('SELECT * FROM Employees', conn)
conn.close()

if df.empty:
    st.warning("No employees found. Please add employees first.")
else:
    st.dataframe(df, use_container_width=True)