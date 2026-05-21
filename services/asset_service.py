import sqlite3
from models.asset import Asset

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Asset]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT 
                assets.id, 
                assets.tag, 
                assets.name, 
                assets.serialNumber, 
                models.name, 
                categories.name, 
                assets.status, 
                assets.description,
                employees.name
            FROM assets
            LEFT JOIN models ON assets.model_id = models.id
            LEFT JOIN categories ON models.category_id = categories.id
            LEFT JOIN checkouts ON assets.id = checkouts.asset_id AND checkouts.is_active = 1
            LEFT JOIN employees ON employees.id = checkouts.employee_id
            WHERE assets.name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT 
                assets.id, 
                assets.tag, 
                assets.name, 
                assets.serialNumber, 
                models.name, 
                categories.name, 
                assets.status, 
                assets.description,
                employees.name
            FROM assets
            LEFT JOIN models ON assets.model_id = models.id
            LEFT JOIN categories ON models.category_id = categories.id
            LEFT JOIN checkouts ON assets.id = checkouts.asset_id AND checkouts.is_active = 1
            LEFT JOIN employees ON employees.id = checkouts.employee_id
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
                description=row[7],
                current_checkout_employee_name=row[8]
            )
        )

    return assets


def insert(
    name, 
    serialNumber, 
    tag, 
    status, 
    model_id, 
    description
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO assets (
            name, 
            serialNumber, 
            tag, 
            status, 
            model_id, 
            description
        ) 
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


def update(
    asset_id, 
    name, 
    serialNumber, 
    tag, 
    status, 
    model_id, 
    description
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE assets SET 
            name=?, 
            serialNumber=?, 
            tag=?, 
            status=?, 
            model_id=?,
            description=?
        WHERE id=?
        """, (
            name, 
            serialNumber, 
            tag, 
            status, 
            model_id, 
            description,
            asset_id
        ))

    conn.commit()
    conn.close()


def delete(cat_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM assets WHERE id=?", (cat_id,))

    conn.commit()
    conn.close()


def count():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM assets")

    total = cur.fetchone()[0]

    conn.close()

    return total

