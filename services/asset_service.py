import sqlite3

DB_NAME = "assets.db"


def get_all(keyword=""):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT assets.tag, assets.name, assets.serialNumber, models.name, categories.name, assets.status 
            FROM assets
            LEFT JOIN models ON assets.model_id = models.id
            LEFT JOIN categories ON models.category_id = categories.id
            WHERE assets.name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT assets.tag, assets.name, assets.serialNumber, models.name, categories.name, assets.status 
            FROM assets
            LEFT JOIN models ON assets.model_id = models.id
            LEFT JOIN categories ON models.category_id = categories.id
        """)

    data = cur.fetchall()
    conn.close()
    return data


def insert(name, serialNumber, tag, status, model_id, description):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO assets (name, serialNumber, tag, status, model_id, description) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        serialNumber,
        tag,
        status,
        model_id,
        description,
    ))

    conn.commit()
    conn.close()


def update(name, serialNumber, tag, status, model_id, description):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("UPDATE assets SET name=? WHERE id=?", (name))

    conn.commit()
    conn.close()


def delete(cat_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM assets WHERE id=?", (cat_id,))

    conn.commit()
    conn.close()
