# utils/advance_utils.py
import pandas as pd
from utils.db_utils import connect_db

def add_advance(employee_id, advance_amount, deduction_date):
    """Add a new advance for an employee."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Advances (employee_id, advance_amount, deduction_date)
    VALUES (?, ?, ?)
    ''', (employee_id, advance_amount, deduction_date))
    conn.commit()
    conn.close()

def get_advances(employee_id):
    """Fetch all advances for a specific employee."""
    conn = connect_db()
    df = pd.read_sql(f'SELECT * FROM Advances WHERE employee_id = "{employee_id}"', conn)
    conn.close()
    return df