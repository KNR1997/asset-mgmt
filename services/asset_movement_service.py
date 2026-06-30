import sqlite3
from models.asset_movement import AssetMovement

DB_NAME = "assets.db"

def get_all(keyword="") -> list[AssetMovement]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    base_query = """
        SELECT
            checkouts.id,
            assets.id,
            assets.tag,
            assets.name,
            models.name,
            categories.name,
            employees.id,
            employees.name,
            checkouts.checkout_date,
            checkouts.expected_checkin_date,
            checkouts.actual_checkin_date,
            checkouts.is_active,
            checkouts.return_condition,
            checkouts.checkout_notes,
            checkouts.return_notes
        FROM checkouts
        LEFT JOIN assets ON checkouts.asset_id = assets.id
        LEFT JOIN employees ON checkouts.employee_id = employees.id
        LEFT JOIN models ON assets.model_id = models.id
        LEFT JOIN categories ON models.category_id = categories.id
    """

    params = ()

    if keyword:
        base_query += """
            WHERE assets.tag LIKE ?
        """
        params = ('%' + keyword + '%',)

    cur.execute(base_query, params)

    rows = cur.fetchall()
    conn.close()

    models = []

    for row in rows:
        models.append(
            AssetMovement(
                checkout_id=row[0],
                asset_id=row[1],
                asset_tag=row[2],
                asset_name=row[3],
                model_name=row[4],
                category_name=row[5],
                employee_id=row[6],
                employee_name=row[7],
                checkout_date=row[8],
                expected_checkin_date=row[9],
                actual_checkin_date=row[10],
                is_active=row[11],
                return_condition=row[12],
                checkout_notes=row[13],
                return_notes=row[14],
            )
        )

    return models