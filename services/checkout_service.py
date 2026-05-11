import sqlite3
from datetime import datetime
from enums.asset_status import AssetStatus

DB_NAME = "assets.db"


def checkout_asset(
    asset_id,
    employee_id,
    expected_checkin_date,
    checkout_notes
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM checkouts
        WHERE asset_id=? AND is_active=1
        """, (asset_id,))

    existing = cur.fetchone()

    if existing:
        raise Exception("Asset already checked out")

    checkout_date = datetime.now().strftime("%Y-%m-%d")

    cur.execute("""
        INSERT INTO checkouts (
            asset_id,
            employee_id,
            checkout_date,
            expected_checkin_date,
            checkout_notes,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        asset_id,
        employee_id,
        checkout_date,
        expected_checkin_date,
        checkout_notes,
        1
    ))

    cur.execute("UPDATE assets SET status=? WHERE id=?",
                (AssetStatus.DEPLOYED, asset_id))

    conn.commit()
    conn.close()


def checkin_asset(
    asset_id, 
    status, 
    return_notes
):
    conn = sqlite3.connect(DB_NAME)

    try:
        cur = conn.cursor()

        # Find active checkout
        cur.execute("""
            SELECT 
                id
            FROM checkouts
            WHERE asset_id=? AND is_active=1
        """, (asset_id,))

        checkout = cur.fetchone()

        if not checkout:
            raise Exception("No active checkout found")

        checkout_id = checkout[0]

        checkin_date = datetime.now().strftime("%Y-%m-%d")

        # Close checkout record
        cur.execute("""
            UPDATE checkouts
            SET
                is_active=0,
                actual_checkin_date=?,
                return_condition=?,
                return_notes=?
            WHERE id=?
        """, (
            checkin_date,
            status,
            return_notes,
            checkout_id
        ))

        # Update asset status
        cur.execute("""
            UPDATE assets
            SET status=?
            WHERE id=?
        """, (
            status,
            asset_id
        ))

        conn.commit()

    finally:
        conn.close()
