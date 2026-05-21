import sqlite3
from models.repair import Repair

DB_NAME = "assets.db"

def insert(
    asset_id, 
    checkout_id, 
    repair_date, 
    repair_cost, 
    status, 
    description,
    notes,
    performed_by,
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
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        asset_id, 
        checkout_id, 
        repair_date, 
        repair_cost, 
        status, 
        description,
        notes,
        performed_by,
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