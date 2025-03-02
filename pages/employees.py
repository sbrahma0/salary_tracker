# pages/Employees.py
import streamlit as st
from utils.employee_utils import add_employee, get_employees
from utils.toast_utils import show_centered_toast

# Page title
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
            # Show custom toast message
            show_centered_toast("Employee added successfully! ✅")
            # Increment the form key to reset the form
            st.session_state.form_key += 1
            st.rerun()
        else:
            st.error("Please fill in all fields.")

    # Handle reset button
    if reset_button:
        # Increment the form key to reset the form
        st.session_state.form_key += 1
        st.rerun()

# Display employee list in a grid layout
st.header("Employee List")
employees = get_employees()

if employees.empty:
    st.warning("No employees found. Please add employees first.")
else:
    # Filter the columns to show only Name, Base Salary, Joining Date, and Designation
    employees = employees[["name", "base_salary", "joining_date", "designation"]]

    # Define the number of columns for the grid
    num_columns = 3  # Adjust this value to control the number of tiles per row
    cols = st.columns(num_columns)

    # Display each employee as a tile in the grid
    for index, row in employees.iterrows():
        with cols[index % num_columns]:
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                ">
                    <h4>{row['name']}</h4>
                    <p><strong>Designation:</strong> {row['designation']}</p>
                    <p><strong>Base Salary:</strong> ₹{row['base_salary']:,.2f}</p>
                    <p><strong>Joining Date:</strong> {row['joining_date']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )