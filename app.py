import datetime
import streamlit as st # type: ignore
import sqlite3
import pandas as pd
import time

# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect('salary.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        employee_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        designation TEXT,
        base_salary REAL,
        joining_date TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
initialize_db()

# Function to connect to the database
def connect_db():
    return sqlite3.connect('salary.db')

# Function to generate the next employee ID
def generate_employee_id():
    conn = connect_db()
    cursor = conn.cursor()
    # Fetch the last employee ID
    cursor.execute('SELECT employee_id FROM Employees ORDER BY employee_id DESC LIMIT 1')
    last_id = cursor.fetchone()
    conn.close()

    if last_id:
        # Extract the numeric part of the last ID and increment it
        last_id_str = last_id[0]  # Ensure it's treated as a string
        last_number = int(last_id_str.split('_')[1])  # Split and extract the numeric part
        new_number = last_number + 1
    else:
        # If no employees exist, start with 1
        new_number = 1

    # Format the new employee ID as EMP_XXXX
    return f"EMP_{new_number:04d}"

# Function to add an employee
def add_employee(name, designation, base_salary, joining_date):
    conn = connect_db()
    cursor = conn.cursor()
    # Generate the employee ID
    employee_id = generate_employee_id()
    # Ensure all data types are correct
    cursor.execute('''
    INSERT INTO Employees (employee_id, name, designation, base_salary, joining_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (str(employee_id), str(name), str(designation), float(base_salary), str(joining_date)))
    conn.commit()
    conn.close()

# Function to fetch all employees
def get_employees():
    conn = connect_db()
    df = pd.read_sql('SELECT * FROM Employees', conn)
    conn.close()
    return df

# Function to fetch salary overview
def get_salary_overview():
    conn = connect_db()
    df = pd.read_sql('''
    SELECT employee_id, name, designation, base_salary, 0 AS total_allowances, 0 AS pending_advance
    FROM Employees
    ''', conn)
    conn.close()
    return df

# Function to display a centered toast message
def show_centered_toast(message):
    st.markdown(
        f"""
        <style>
        .centered-toast {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            border-radius: 5px;
            z-index: 1000;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
        }}
        </style>
        <div class="centered-toast">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Automatically remove the toast after 2 seconds
    time.sleep(2)
    #st.rerun()

# Streamlit app
st.set_page_config(page_title="Employee Salary Dashboard", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", ["Dashboard", "Employees", "Reports", "Salary Management"])

# About section in the sidebar
st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.write("This is an INR-based employee salary management system that helps track salaries, deductions, and advances.")

# Main content based on selected page
if page == "Dashboard":
    st.title("Employee Salary Dashboard")
    st.header("Employee Salary Overview")

    # Fetch and display salary overview
    salary_overview = get_salary_overview()
    st.dataframe(salary_overview, use_container_width=True)

elif page == "Employees":
    st.title("Employee Management")
    st.header("Add Employee")

    # Initialize session state for form reset
    if 'form_key' not in st.session_state:
        st.session_state.form_key = 0

    # Form to add an employee
    with st.form("employee_form"):
        # Use a unique key for each form field
        name = st.text_input("Employee Name", key=f"name_{st.session_state.form_key}")
        designation = st.text_input("Designation", key=f"designation_{st.session_state.form_key}")
        base_salary = st.number_input("Base Salary (INR)", min_value=0.0, key=f"base_salary_{st.session_state.form_key}")
        joining_date = st.date_input("Joining Date", key=f"joining_date_{st.session_state.form_key}")

        # Two buttons: Reset and Add Employee
        col1, col2 = st.columns(2)
        with col1:
            reset_button = st.form_submit_button("Reset")
        with col2:
            add_button = st.form_submit_button("Add Employee")

        # Handle form submission
        if add_button:
            if name and designation and base_salary and joining_date:
                
                add_employee(name, designation, base_salary, joining_date.strftime('%Y-%m-%d'))
                #st.success("Employee added successfully!")
                #st.toast("Employee added successfully!", icon="✅")
                #time.sleep(2)
                show_centered_toast("Employee added successfully! ✅")
                #time.sleep(2)
                st.session_state.form_key += 1 
                st.rerun()
                
                # Reset the form fields by changing the form key
                
                
            else:
                st.error("Please fill in all fields.")

        # Handle reset button
        if reset_button:
            # Reset the form fields by changing the form key
            st.session_state.form_key += 1
            st.rerun()

    # Display employee table
    st.header("Employee List")
    employees = get_employees()
    if employees.empty:
        st.warning("No employees found. Please add employees first.")
    else:
        st.dataframe(employees, use_container_width=True)

elif page == "Reports":
    st.title("Salary Reports")
    st.write("Salary reports will be displayed here.")

elif page == "Salary Management":
    st.title("Salary Management")
    st.write("Manage deductions, advances, and monthly deductions here.")
