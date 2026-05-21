import sqlite3
from models.license import License

DB_NAME = "assets.db"


def get_all(keyword="") -> list[License]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT
                licenses.id,
                licenses.softwareName,
                licenses.categoryName,
                licenses.seats
            FROM licenses
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT
                licenses.id,
                licenses.softwareName,
                licenses.categoryName,
                licenses.seats
            FROM licenses
        """)

    rows = cur.fetchall()
    conn.close()

    licenses = []

    for row in rows:
        licenses.append(
            License(
                id=row[0],
                softwareName=row[1],
                categoryName=row[2],
                seats=row[3],
            )
        )

    return licenses


def insert(
    softwareName,
    categoryName,
    seats
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO licenses (
            softwareName,
            categoryName,
            seats
        )
        VALUES (?, ?, ?)
    """, (
        softwareName,
        categoryName,
        seats
    ))

    conn.commit()
    conn.close()


def update(
    license_id, 
    softwareName,
    categoryName,
    seats
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE licenses SET
            softwareName=?,
            categoryName=?,
            seats=?
        WHERE id=?
        """, (
            softwareName,
            categoryName,
            seats,
            license_id
        ))

    conn.commit()
    conn.close()


def delete(license_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM licenses WHERE id=?", (license_id,))

    conn.commit()
    conn.close()



def count():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM licenses")

    total = cur.fetchone()[0]

    conn.close()

    return total
