import sqlite3
from models.asset import Asset

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Asset]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT assets.id, assets.tag, assets.name, assets.serialNumber, models.name, categories.name, assets.status, assets.description 
            FROM assets
            LEFT JOIN models ON assets.model_id = models.id
            LEFT JOIN categories ON models.category_id = categories.id
            WHERE assets.name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT assets.id, assets.tag, assets.name, assets.serialNumber, models.name, categories.name, assets.status, assets.description 
            FROM assets
            LEFT JOIN models ON assets.model_id = models.id
            LEFT JOIN categories ON models.category_id = categories.id
        """)

    rows = cur.fetchall()
    conn.close()

    assets = []

    for row in rows:
        assets.append(
            Asset(
                id=row[0],
                tag=row[1],
                name=row[2],
                serial_number=row[3],
                model_name=row[4],
                category_name=row[5],
                status=row[6],
                description=row[7]
            )
        )

    return assets


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


def update(asset_id, name, serialNumber, tag, status, model_id, description):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("UPDATE assets SET name=?, serialNumber=?, tag=?, status=?, model_id=?, description=? WHERE id=?", 
                (name, serialNumber, tag, status, model_id, description, asset_id))

    conn.commit()
    conn.close()


def delete(cat_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM assets WHERE id=?", (cat_id,))

    conn.commit()
    conn.close()
