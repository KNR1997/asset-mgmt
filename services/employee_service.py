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
                department,
                email,
                contactNumber
            FROM employees
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT
                id, 
                name, 
                department,
                email,
                contactNumber
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
                email=row[3],
                contact_number=row[4],
            )
        )

    return employees


def get_by_name(name):
    """Get employee by name"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM employees WHERE name = ?", (name,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def get_by_email(email):
    """Get employee by email"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM employees WHERE email = ?", (email,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def get_by_contact_number(contact_number):
    """Get employee by contact_number"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM employees WHERE contact_number = ?", (contact_number,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def insert(
    name, 
    department,
    email,
    contact_number,
):
    # Validate uniqueness before insert
    if get_by_name(name):
        raise ValueError(f"Employee with name '{name}' already exists")

    # Validate uniqueness before insert
    if get_by_email(email):
        raise ValueError(f"Employee with email '{email}' already exists")

    # Validate uniqueness before insert
    if get_by_contact_number(contact_number):
        raise ValueError(f"Employee with contact number '{contact_number}' already exists")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO employees (
            name, 
            department,
            email,
            contactNumber
        )
        VALUES (?, ?, ?, ?)
    """, (
        name,
        department,
        email,
        contact_number,
    ))

    conn.commit()
    conn.close()


def update(
    employee_id, 
    name, 
    department,
    email,
    contact_number,
):
    # When updating, exclude the current asset from uniqueness check
    existing_by_name = get_by_name(name)
    if existing_by_name and existing_by_name['id'] != employee_id:
        raise ValueError(f"Employee with name '{name}' already exists")

    existing_by_email = get_by_email(email)
    if existing_by_email and existing_by_email['id'] != employee_id:
        raise ValueError(f"Employee with email '{email}' already exists")

    existing_by_contact_number = get_by_contact_number(contact_number)
    if existing_by_contact_number and existing_by_contact_number['id'] != employee_id:
        raise ValueError(f"Employee with contact number '{contact_number}' already exists")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE employees SET
            name=?,
            department=?,
            email=?,
            contactNumber=?
        WHERE id=?
        """, (
            name, 
            department,
            email,
            contact_number,
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
