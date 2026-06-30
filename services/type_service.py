import sqlite3
from models.type import Type

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Type]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    base_query = """
        SELECT
            id, 
            name 
        FROM types
    """

    params = ()

    if keyword:
        base_query += """
            WHERE types.name LIKE ?
        """
        params = ('%' + keyword + '%',)

    cur.execute(base_query, params)

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
