import sqlite3
from models.category import Category

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Category]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT
                id, 
                name, 
                description
            FROM categories
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT
                id, 
                name, 
                description
            FROM categories
        """)

    rows = cur.fetchall()
    conn.close()

    categories = []

    for row in rows:
        categories.append(
            Category(
                id=row[0],
                name=row[1],
                description=row[2]
            )
        )

    return categories


def insert(
    name, 
    description
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO categories (
            name, 
            description
        )
        VALUES (?, ?)
    """, (
        name,
        description
    ))

    conn.commit()
    conn.close()


def update(
    category_id, 
    name
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE categories SET
            name=?,
        WHERE id=?
        """, (
            name, 
            category_id
        ))

    conn.commit()
    conn.close()


def delete(cat_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM categories WHERE id=?", (cat_id,))

    conn.commit()
    conn.close()
