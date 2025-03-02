# utils/employee_utils.py
import pandas as pd
from utils.db_utils import connect_db

def generate_employee_id():
    """Generate a new employee ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT employee_id FROM Employees ORDER BY employee_id DESC LIMIT 1')
    last_id = cursor.fetchone()
    conn.close()

    if last_id:
        last_number = int(last_id[0].split('_')[1])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"EMP_{new_number:04d}"

def add_employee(name, designation, base_salary, joining_date):
    """Add a new employee to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    employee_id = generate_employee_id()
    cursor.execute('''
    INSERT INTO Employees (employee_id, name, designation, base_salary, joining_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (employee_id, name, designation, base_salary, joining_date))
    conn.commit()
    conn.close()

def get_employees():
    """Fetch all employees from the database."""
    conn = connect_db()
    df = pd.read_sql('SELECT * FROM Employees', conn)
    conn.close()
    return df