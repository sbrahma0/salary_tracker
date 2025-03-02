# app.py
import streamlit as st
from utils.db_utils import initialize_db

# Initialize the database
initialize_db()

# Streamlit app
st.set_page_config(page_title="Employee Salary Dashboard", layout="wide")

# About section on the main page
st.header("About")
st.write("This is an INR-based employee salary management system that helps track salaries, deductions, and advances.")