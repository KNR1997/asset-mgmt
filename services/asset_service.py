import sqlite3
from models.asset import Asset

DB_NAME = "assets.db"


def get_all(keyword="", status="All") -> list[Asset]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    query = """
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
        LEFT JOIN checkouts 
            ON assets.id = checkouts.asset_id 
            AND checkouts.is_active = 1
        LEFT JOIN employees 
            ON employees.id = checkouts.employee_id
        WHERE 1=1
    """

    params = []

    if keyword:
        query += " AND assets.name LIKE ?"
        params.append(f"%{keyword}%")

    if status != "All":
        query += " AND assets.status = ?"
        params.append(status)

    cur.execute(query, params)

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

def get_by_tag(tag):
    """Get asset by tag"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM assets WHERE tag = ?", (tag,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def get_by_serial(serial_number):
    """Get asset by serial number"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM assets WHERE serialNumber = ?", (serial_number,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None

def insert(
    name, 
    serialNumber, 
    tag, 
    status, 
    model_id, 
    description
):
    # Validate uniqueness before insert
    if get_by_tag(tag):
        raise ValueError(f"Asset with tag '{tag}' already exists")

    if get_by_serial(serialNumber):
        raise ValueError(f"Asset with serial number '{serialNumber}' already exists")

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
    # When updating, exclude the current asset from uniqueness check
    existing_by_tag = get_by_tag(tag)
    if existing_by_tag and existing_by_tag['id'] != asset_id:
        raise ValueError(f"Asset with tag '{tag}' already exists")

    existing_by_serial = get_by_serial(serialNumber)
    if existing_by_serial and existing_by_serial['id'] != asset_id:
        raise ValueError(f"Asset with serial number '{serialNumber}' already exists")

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


def get_all_broken(keyword="") -> list[Asset]:
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
            WHERE assets.status == 'Broken' AND assets.name LIKE ?
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
            WHERE assets.status == 'Broken'
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

def update_status(
    asset_id,
    status,
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE assets SET 
            status=?
        WHERE id=?
        """, (
            status, 
            asset_id
        ))

    conn.commit()
    conn.close()
