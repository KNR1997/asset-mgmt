import sqlite3

DB_NAME = "assets.db"


def get_all(keyword=""):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("SELECT * FROM employees WHERE name LIKE ?",
                    ('%' + keyword + '%',))
    else:
        cur.execute("SELECT * FROM employees")

    data = cur.fetchall()
    conn.close()
    return data


def insert(name, department):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO employees (name, department) VALUES (?, ?)", (name, department))

    conn.commit()
    conn.close()


def update(name, department):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("UPDATE employees SET name=? WHERE id=?", (name))

    conn.commit()
    conn.close()


def delete(emp_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))

    conn.commit()
    conn.close()
