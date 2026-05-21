import sqlite3
from models.type import Type

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Type]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT
                id, 
                name
            FROM types
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT
                id, 
                name 
            FROM types
        """)

    rows = cur.fetchall()
    conn.close()

    types = []

    for row in rows:
        types.append(
            Type(
                id=row[0],
                name=row[1],
            )
        )

    return types
