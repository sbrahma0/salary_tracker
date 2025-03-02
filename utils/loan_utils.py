# utils/loan_utils.py
import pandas as pd
from utils.db_utils import connect_db

def add_loan(employee_id, loan_amount, monthly_deduction, start_date, end_date):
    """Add a new loan for an employee."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Loans (employee_id, loan_amount, monthly_deduction, start_date, end_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (employee_id, loan_amount, monthly_deduction, start_date, end_date))
    conn.commit()
    conn.close()

def get_loans(employee_id):
    """Fetch all loans for a specific employee."""
    conn = connect_db()
    df = pd.read_sql(f'SELECT * FROM Loans WHERE employee_id = "{employee_id}"', conn)
    conn.close()
    return df