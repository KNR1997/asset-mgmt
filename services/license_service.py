import sqlite3
from models.license import License

DB_NAME = "assets.db"


def get_all(keyword="") -> list[License]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    base_query = """
        SELECT 
            licenses.id,
            licenses.softwareName,
            licenses.categoryName,
            licenses.seats,
            licenses.minQuantity,
            licenses.productKey,
            licenses.licensedTo,
            licenses.licensedToEmail,
            licenses.orderNumber,
            licenses.purchaseCost,
            licenses.purchaseDate,
            licenses.expirationDate,
            licenses.terminationDate,
            licenses.notes,
            manufacturers.id,
            manufacturers.name
        FROM licenses
        LEFT JOIN manufacturers 
            ON licenses.manufacturer_id = manufacturers.id
    """

    params = ()

    if keyword:
        base_query += """
            WHERE licenses.softwareName LIKE ?
        """
        params = ('%' + keyword + '%',)

    cur.execute(base_query, params)

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
                minQuantity=row[4],
                productKey=row[5],
                licensedTo=row[6],
                licensedToEmail=row[7],
                orderNumber=row[8],
                purchaseCost=row[9],
                purchaseDate=row[10],
                expirationDate=row[11],
                terminationDate=row[12],
                notes=row[13],
                manufacturer_id=row[14],
                manufacturer_name=row[15]
            )
        )

    return licenses


def insert(
    softwareName,
    categoryName,
    seats,
    productKey,
    licensedTo,
    licensedToEmail,
    orderNumber,
    purchaseCost,
    purchaseDate,
    expirationDate,
    # terminationDate,
    manufacturer_id,
    notes
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO licenses (
            softwareName,
            categoryName,
            seats,
            productKey,
            licensedTo,
            licensedToEmail,
            orderNumber,
            purchaseCost,
            purchaseDate,
            expirationDate,
            manufacturer_id,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        softwareName,
        categoryName,
        seats,
        productKey,
        licensedTo,
        licensedToEmail,
        orderNumber,
        purchaseCost,
        purchaseDate,
        expirationDate,
        # terminationDate,
        manufacturer_id,
        notes
    ))

    conn.commit()
    conn.close()


def update(
    license_id, 
    softwareName,
    categoryName,
    seats,
    productKey,
    licensedTo,
    licensedToEmail,
    orderNumber,
    purchaseCost,
    purchaseDate,
    expirationDate,
    # terminationDate,
    manufacturer_id,
    notes
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE licenses SET
            softwareName=?,
            categoryName=?,
            seats=?,
            productKey=?,
            licensedTo=?,
            licensedToEmail=?, 
            orderNumber=?,
            purchaseCost=?,
            purchaseDate=?,
            expirationDate=?,
            manufacturer_id=?,    
            notes=?
        WHERE id=?
        """, (
            softwareName,
            categoryName,
            seats,
            productKey,
            licensedTo,
            licensedToEmail,
            orderNumber,
            purchaseCost,
            purchaseDate,
            expirationDate,
            # terminationDate,
            manufacturer_id,
            notes,
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
