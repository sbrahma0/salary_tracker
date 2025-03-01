import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('salary.db')
cursor = conn.cursor()

# Drop the Employees table if it exists
cursor.execute('DROP TABLE IF EXISTS Employees')

# Create Employees table with the updated schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    designation TEXT,
    base_salary REAL,
    joining_date TEXT
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")