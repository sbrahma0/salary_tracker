# utils/db_utils.py
import sqlite3

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect('salary.db')

def initialize_db():
    """Initialize the database and create tables if they don't exist."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Create Employees table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employees (
        employee_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        designation TEXT,
        base_salary REAL,
        joining_date TEXT
    )
    ''')
    
    # Create Loans table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Loans (
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        loan_amount REAL,
        monthly_deduction REAL,
        start_date TEXT,
        end_date TEXT,
        FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
    )
    ''')
    
    # Create Advances table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Advances (
        advance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        advance_amount REAL,
        deduction_date TEXT,
        FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
    )
    ''')
    
    # Create Deductions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Deductions (
        deduction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        deduction_amount REAL,
        deduction_reason TEXT,
        deduction_date TEXT,
        FOREIGN KEY (employee_id) REFERENCES Employees (employee_id)
    )
    ''')
    
    conn.commit()
    conn.close()