# pages/Salary_Management.py
import streamlit as st
import pandas as pd
from utils.db_utils import connect_db
from utils.loan_utils import add_loan, get_loans
from utils.advance_utils import add_advance, get_advances
from utils.deduction_utils import add_deduction, get_deductions

# Page title
st.title("Salary Management")
st.write("Manage loans, advances, and deductions for employees.")

# Fetch all employees for selection
conn = connect_db()
employees = pd.read_sql('SELECT * FROM Employees', conn)
conn.close()

if employees.empty:
    st.warning("No employees found. Please add employees first.")
else:
    # Select employee by name
    employee_names = employees['name'].tolist()
    selected_employee = st.selectbox("Select Employee", employee_names, key="select_employee")

    # Get the selected employee's ID
    selected_employee_id = employees[employees['name'] == selected_employee]['employee_id'].values[0]

    # Dropdown to select transaction type
    transaction_type = st.selectbox(
        "Select Transaction Type",
        ["Loan", "Advance", "Deduction/Penalty"],
        key="transaction_type"
    )

    # Display the appropriate form based on the selected transaction type
    if transaction_type == "Loan":
        st.header("Add Loan")
        loan_amount = st.number_input("Loan Amount (INR)", min_value=0.0, key="loan_amount")
        monthly_deduction = st.number_input("Monthly Deduction (INR)", min_value=0.0, key="monthly_deduction")
        loan_start_date = st.date_input("Loan Start Date", key="loan_start_date")
        loan_end_date = st.date_input("Loan End Date", key="loan_end_date")

        if st.button("Add Loan", key="add_loan"):
            if loan_amount > 0 and monthly_deduction > 0:
                add_loan(selected_employee_id, loan_amount, monthly_deduction, loan_start_date.strftime('%Y-%m-%d'), loan_end_date.strftime('%Y-%m-%d'))
                st.success("Loan added successfully!")
            else:
                st.error("Please enter valid loan details.")

    elif transaction_type == "Advance":
        st.header("Add Advance Payment")
        advance_amount = st.number_input("Advance Amount (INR)", min_value=0.0, key="advance_amount")
        deduction_date = st.date_input("Deduction Date", key="advance_deduction_date")

        if st.button("Add Advance", key="add_advance"):
            if advance_amount > 0:
                add_advance(selected_employee_id, advance_amount, deduction_date.strftime('%Y-%m-%d'))
                st.success("Advance added successfully!")
            else:
                st.error("Please enter a valid advance amount.")

    elif transaction_type == "Deduction/Penalty":
        st.header("Add Deduction/Penalty")
        deduction_amount = st.number_input("Deduction Amount (INR)", min_value=0.0, key="deduction_amount")
        deduction_reason = st.text_input("Reason for Deduction", key="deduction_reason")
        deduction_date = st.date_input("Deduction Date", key="penalty_deduction_date")

        if st.button("Add Deduction", key="add_deduction"):
            if deduction_amount > 0 and deduction_reason:
                add_deduction(selected_employee_id, deduction_amount, deduction_reason, deduction_date.strftime('%Y-%m-%d'))
                st.success("Deduction added successfully!")
            else:
                st.error("Please enter valid deduction details.")

    # Display Active Transactions
    st.header("Active Transactions")

    # Fetch and display loans
    loans = get_loans(selected_employee_id)
    st.subheader("Loans")
    if loans.empty:
        st.write("No active loans.")
    else:
        st.dataframe(loans)

    # Fetch and display advances
    advances = get_advances(selected_employee_id)
    st.subheader("Advances")
    if advances.empty:
        st.write("No active advances.")
    else:
        st.dataframe(advances)

    # Fetch and display deductions
    deductions = get_deductions(selected_employee_id)
    st.subheader("Deductions")
    if deductions.empty:
        st.write("No active deductions.")
    else:
        st.dataframe(deductions)