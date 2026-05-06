import sqlite3

DB_NAME = "assets.db"


def get_all(keyword=""):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT models.id, models.name, models.modelNumber, categories.name
            FROM models
            LEFT JOIN categories ON models.category_id = categories.id
            WHERE models.name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT models.id, models.name, models.modelNumber, categories.name
            FROM models
            LEFT JOIN categories ON models.category_id = categories.id
        """)

    data = cur.fetchall()
    conn.close()
    return data


def insert(name, model_id, desc, category_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO models (name, modelNumber, description, category_id)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        model_id,
        desc,
        category_id,
    ))

    conn.commit()
    conn.close()


def update(name, model_id, desc, category_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("UPDATE models SET name=? WHERE id=?",
                (name, model_id, desc, category_id))

    conn.commit()
    conn.close()


def delete(asset_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM models WHERE id=?", (asset_id,))

    conn.commit()
    conn.close()
