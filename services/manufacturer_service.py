import sqlite3
from models.manufacturer import Manufacturer

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Manufacturer]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT
                id, 
                name, 
                url,
                supportURL,
                supportPhone,
                warrantyLookupUrl,
                supportEmail,
                notes
            FROM manufacturers
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT
                id, 
                name, 
                url,
                supportURL,
                supportPhone,
                warrantyLookupUrl,
                supportEmail,
                notes
            FROM manufacturers
        """)

    rows = cur.fetchall()
    conn.close()

    manufacturers = []

    for row in rows:
        manufacturers.append(
            Manufacturer(
                id=row[0],
                name=row[1],
                url=row[2],
                supportURL=row[3],
                supportPhone=row[4],
                warrantyLookupUrl=row[5],
                supportEmail=row[6],
                notes=row[7],
            )
        )

    return manufacturers


def get_by_name(name):
    """Get manufacturer by name"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM manufacturers WHERE name = ?", (name,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None


def insert(
    name,
    url,
    supportURL,
    supportPhone,
    warrantyLookupUrl,
    supportEmail,
    notes
):
    # Validate uniqueness before insert
    if get_by_name(name):
        raise ValueError(f"Manufacturer with name '{name}' already exists")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO manufacturers (
            name, 
            url, 
            supportURL, 
            supportPhone, 
            warrantyLookupUrl, 
            supportEmail, 
            notes
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        url,
        supportURL,
        supportPhone,
        warrantyLookupUrl,
        supportEmail,
        notes
    ))

    conn.commit()
    conn.close()


def update(
    manufacturer_id,
    name,
    url,
    supportURL,
    supportPhone,
    warrantyLookupUrl,
    supportEmail,
    notes
):
    # When updating, exclude the current asset from uniqueness check
    existing_by_name = get_by_name(name)
    if existing_by_name and existing_by_name['id'] != manufacturer_id:
        raise ValueError(f"Manufacturer with name '{name}' already exists")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE manufacturers SET 
            name=?, 
            url=?, 
            supportURL=?, 
            supportPhone=?, 
            warrantyLookupUrl=?, 
            supportEmail=?, 
            notes=? 
        WHERE id=?
    """, (
        name,
        url,
        supportURL,
        supportPhone,
        warrantyLookupUrl,
        supportEmail,
        notes,
        manufacturer_id
    ))

    conn.commit()
    conn.close()


def delete(manufacturer_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM manufacturers WHERE id=?", (manufacturer_id,))

    conn.commit()
    conn.close()
