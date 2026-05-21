import sqlite3
from models.accessory import Accessory

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Accessory]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT
                accessories.id,
                accessories.accessoryName,
                accessories.categoryName,
                accessories.supplierName,
                accessories.modelNumber,
                accessories.minQuantity,
                accessories.orderNumber,
                accessories.unitCost,
                accessories.purchaseDate,
                accessories.qunatity,
                accessories.notes
            FROM accessories
            WHERE name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT
                accessories.id,
                accessories.accessoryName,
                accessories.categoryName,
                accessories.supplierName,
                accessories.modelNumber,
                accessories.minQuantity,
                accessories.orderNumber,
                accessories.unitCost,
                accessories.purchaseDate,
                accessories.qunatity,
                accessories.notes
            FROM accessories
        """)

    rows = cur.fetchall()
    conn.close()

    accessories = []

    for row in rows:
        accessories.append(
            Accessory(
                id=row[0],
                accessoryName=row[1],
                categoryName=row[2],
                supplierName=row[3],
                modelNumber=row[4],
                minQuantity=row[5],
                orderNumber=row[6],
                unitCost=row[7],
                purchaseDate=row[8],
                qunatity=row[9],
                notes=row[10],
            )
        )

    return accessories


def insert(
    accessoryName,
    categoryName,
    supplierName,
    modelNumber,
    minQuantity,
    qunatity,
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO accessories (
            accessoryName,
            categoryName,
            supplierName,
            modelNumber,
            minQuantity,
            qunatity
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        accessoryName,
        categoryName,
        supplierName,
        modelNumber,
        minQuantity,
        qunatity,
    ))

    conn.commit()
    conn.close()


def update(
    accessory_id, 
    accessoryName,
    categoryName,
    supplierName,
    modelNumber,
    minQuantity,
    qunatity,
):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE accessories SET
            accessoryName=?,
            categoryName=?,
            supplierName=?,
            modelNumber=?,
            minQuantity=?,
            qunatity=?
        WHERE id=?
        """, (
            accessoryName,
            categoryName,
            supplierName,
            accessory_id,
            modelNumber,
            minQuantity,
            qunatity,
        ))

    conn.commit()
    conn.close()


def delete(accessory_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM accessories WHERE id=?", (accessory_id,))

    conn.commit()
    conn.close()



def count():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM accessories")

    total = cur.fetchone()[0]

    conn.close()

    return total
