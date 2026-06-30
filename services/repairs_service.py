import sqlite3
from models.repair import Repair

DB_NAME = "assets.db"

def get_all(keyword="", from_date="", to_date="") -> list[Repair]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    base_query = """
        SELECT 
            repairs.id, 
            repairs.repair_date, 
            repairs.repair_cost,
            repairs.status, 
            repairs.description, 
            repairs.notes, 
            repairs.performed_by, 
            repairs.warranty_covered,
            assets.id,
            assets.tag,
            assets.serialNumber,
            models.name,
            categories.name,
            checkouts.id
        FROM repairs
        LEFT JOIN assets ON repairs.asset_id = assets.id
        LEFT JOIN models ON assets.model_id = models.id
        LEFT JOIN categories ON models.category_id = categories.id
        LEFT JOIN checkouts ON repairs.checkout_id = checkouts.id
    """

    conditions = []
    params = []

    if keyword:
            conditions.append("assets.tag LIKE ?")
            params.append('%' + keyword + '%')

    if from_date:
            conditions.append("repairs.repair_date >= ?")
            params.append(from_date)

    if to_date:
        conditions.append("repairs.repair_date <= ?")
        params.append(to_date)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

# Add ORDER BY to show latest repairs first
    base_query += " ORDER BY repairs.repair_date DESC"

    cur.execute(base_query, params)

    rows = cur.fetchall()
    conn.close()

    repairs = []

    for row in rows:
        repairs.append(
            Repair(
                id=row[0],
                repair_date=row[1],
                repair_cost=row[2],
                status=row[3],
                description=row[4],
                notes=row[5],
                performed_by=row[6],
                warranty_covered=row[7],
                asset_id=row[8],
                asset_tag=row[9],
                asset_serial_number=row[10],
                asset_model_name=row[11],
                asset_category_name=row[12],
                checkout_id=row[13],
            )
        )

    return repairs

def insert(
    asset_id, 
    checkout_id, 
    repair_date, 
    repair_cost, 
    status, 
    description,
    notes,
    performed_by,
    warranty_covered,
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO repairs (
            asset_id, 
            checkout_id, 
            repair_date, 
            repair_cost, 
            status, 
            description,
            notes,
            performed_by,
            warranty_covered
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        asset_id, 
        checkout_id, 
        repair_date, 
        repair_cost, 
        status, 
        description,
        notes,
        performed_by,
        warranty_covered,
    ))

    conn.commit()
    conn.close()


def update(
    repair_id,
    asset_id, 
    name, 
    serialNumber, 
    tag, 
    status, 
    model_id, 
    description,
    notes,
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE repairs SET 
            asset_id=?, 
            checkout_id=?, 
            repair_date=?, 
            repair_cost=?, 
            status=?, 
            description=?,
            notes=?,
            performed_by=?,
        WHERE id=?
        """, (
            asset_id, 
            name, 
            serialNumber, 
            tag, 
            status, 
            model_id, 
            description,
            notes,
            repair_id,
        ))

    conn.commit()
    conn.close()