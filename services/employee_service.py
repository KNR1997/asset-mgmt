import sqlite3
from models.employee import Employee

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Employee]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT
                id, 
                name, 
                department
            FROM employees
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT
                id, 
                name, 
                department
            FROM employees
        """)

    rows = cur.fetchall()
    conn.close()

    employees = []

    for row in rows:
        employees.append(
            Employee(
                id=row[0],
                name=row[1],
                department=row[2],
            )
        )

    return employees


def insert(
    name, 
    department
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO employees (
            name, 
            department
        )
        VALUES (?, ?)
    """, (
        name,
        department
    ))

    conn.commit()
    conn.close()


def update(
    employee_id, 
    name, 
    department
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE employees SET
            name=?,
            department=?
        WHERE id=?
        """, (
            name, 
            department,
            employee_id
        ))

    conn.commit()
    conn.close()


def delete(emp_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))

    conn.commit()
    conn.close()


def count():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM employees")

    total = cur.fetchone()[0]

    conn.close()

    return total
