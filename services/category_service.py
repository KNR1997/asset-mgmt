import sqlite3
from models.category import Category

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Category]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT
                categories.id,
                categories.name,
                categories.description,
                types.name
            FROM categories
            LEFT JOIN types ON categories.type_id = types.id
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT
                categories.id,
                categories.name,
                categories.description,
                types.name
            FROM categories
            LEFT JOIN types ON categories.type_id = types.id
        """)

    rows = cur.fetchall()
    conn.close()

    categories = []

    for row in rows:
        categories.append(
            Category(
                id=row[0],
                name=row[1],
                description=row[2],
                type_name=row[3]
            )
        )

    return categories


def insert(
    name,
    type_id,
    description
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO categories (
            name,
            type_id,
            description
        )
        VALUES (?, ?, ?)
    """, (
        name,
        type_id,
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
