import streamlit as st
import sqlite3


st.set_page_config(
    page_title="Employee Record System",
    page_icon="💼",
    layout="wide"
)


conn = sqlite3.connect("employees.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    department TEXT,
    salary INTEGER
)
""")
conn.commit()


st.title("💼 Employee Management System")
st.caption("Manage Employee Information Easily")


menu = st.radio(
    "Navigation",
    [
        "➕ Register Employee",
        "👥 Employee Records",
        "📝 Edit Employee",
        "❌ Remove Employee",
        "👤 About Me"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

if menu == "➕ Register Employee":

    st.header("➕ Register New Employee")

    name = st.text_input("Employee Name")
    email = st.text_input("Email Address")

    department = st.selectbox(
        "Department",
        ["IT", "HR", "Finance", "Marketing", "Management", "Other"]
    )

    salary = st.number_input(
        "Monthly Salary",
        min_value=0,
        step=1000
    )

    if st.button("Register Employee", type="primary"):

        if name and email:

            cur.execute("""
            INSERT INTO employees (name, email, department, salary)
            VALUES (?, ?, ?, ?)
            """, (name, email, department, salary))

            conn.commit()

            st.success("Employee Registered Successfully!")

        else:
            st.warning("Please enter employee name and email.")


elif menu == "👥 Employee Records":

    st.header("👥 Employee Records")

    cur.execute("SELECT * FROM employees")
    records = cur.fetchall()

    if records:

        st.write("Total Employees:", len(records))

        for employee in records:

            with st.expander(
                f"👤 {employee[1]} - {employee[3]}"
            ):

                st.write("**Employee ID:**", employee[0])
                st.write("**Name:**", employee[1])
                st.write("**Email:**", employee[2])
                st.write("**Department:**", employee[3])
                st.write("**Monthly Salary:**", employee[4])

    else:
        st.info("No employee records found.")


elif menu == "📝 Edit Employee":

    st.header("📝 Update Employee Information")

    emp_id = st.number_input(
        "Enter Employee ID",
        min_value=1,
        step=1
    )

    new_name = st.text_input("New Employee Name")
    new_email = st.text_input("New Email Address")

    new_department = st.selectbox(
        "New Department",
        ["IT", "HR", "Finance", "Marketing", "Management", "Other"]
    )

    new_salary = st.number_input(
        "New Monthly Salary",
        min_value=0,
        step=1000
    )

    if st.button("Save Changes", type="primary"):

        if new_name and new_email:

            cur.execute("""
            UPDATE employees
            SET name=?, email=?, department=?, salary=?
            WHERE id=?
            """, (
                new_name,
                new_email,
                new_department,
                new_salary,
                emp_id
            ))

            conn.commit()

            if cur.rowcount > 0:
                st.success("Employee Information Updated Successfully!")
            else:
                st.warning("Employee ID Not Found.")

        else:
            st.warning("Please enter employee name and email.")


# 4. Remove Employee
elif menu == "❌ Remove Employee":

    st.header("❌ Remove Employee")

    emp_id = st.number_input(
        "Enter Employee ID",
        min_value=1,
        step=1
    )

    st.warning("This action will permanently delete the employee record.")

    if st.button("Delete Employee", type="primary"):

        cur.execute(
            "DELETE FROM employees WHERE id=?",
            (emp_id,)
        )

        conn.commit()

        if cur.rowcount > 0:
            st.success("Employee Deleted Successfully!")
        else:
            st.warning("Employee ID Not Found.")


# 5. About Me
elif menu == "👤 About Me":

    st.header("👤 About Me")

    st.subheader("MD Ramim")

    st.write("**Department:** Computer Science and Technology (CST)")
    st.write("**Institute:** Brahmanbaria Polytechnic Institute")

    st.divider()

    st.subheader("My Interests")

    st.write("- Python Programming")
    st.write("- Web Development")


    st.divider()

    st.subheader("Technologies Used")

    st.write("- Python")
    st.write("- Streamlit")
    st.write("- SQLite")


conn.close()
