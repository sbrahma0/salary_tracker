import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('salary.db')
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS Employees')
cursor.execute('DROP TABLE IF EXISTS Loans')
cursor.execute('DROP TABLE IF EXISTS Advances')
cursor.execute('DROP TABLE IF EXISTS Deductions')

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

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")