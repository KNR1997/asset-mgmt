import sqlite3

DB_NAME = "assets.db"


def get_all(keyword=""):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("SELECT * FROM categories WHERE name LIKE ?",
                    ('%' + keyword + '%',))
    else:
        cur.execute("SELECT * FROM categories")

    data = cur.fetchall()
    conn.close()
    return data


def insert(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO categories (name, description) VALUES (?, ?)", (name, "desc"))

    conn.commit()
    conn.close()


def update(cat_id, name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("UPDATE categories SET name=? WHERE id=?", (name, cat_id))

    conn.commit()
    conn.close()


def delete(cat_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM categories WHERE id=?", (cat_id,))

    conn.commit()
    conn.close()
