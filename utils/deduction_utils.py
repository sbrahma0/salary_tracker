# utils/deduction_utils.py
import pandas as pd
from utils.db_utils import connect_db

def add_deduction(employee_id, deduction_amount, deduction_reason, deduction_date):
    """Add a new deduction for an employee."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Deductions (employee_id, deduction_amount, deduction_reason, deduction_date)
    VALUES (?, ?, ?, ?)
    ''', (employee_id, deduction_amount, deduction_reason, deduction_date))
    conn.commit()
    conn.close()

def get_deductions(employee_id):
    """Fetch all deductions for a specific employee."""
    conn = connect_db()
    df = pd.read_sql(f'SELECT * FROM Deductions WHERE employee_id = "{employee_id}"', conn)
    conn.close()
    return df