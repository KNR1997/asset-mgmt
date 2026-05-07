import sqlite3
from models.model import Model

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Model]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if keyword:
        cur.execute("""
            SELECT models.id, models.name, models.modelNumber, categories.id, categories.name, models.description
            FROM models
            LEFT JOIN categories ON models.category_id = categories.id
            WHERE models.name LIKE ?
        """, ('%' + keyword + '%',))
    else:
        cur.execute("""
            SELECT models.id, models.name, models.modelNumber, categories.id, categories.name, models.description
            FROM models
            LEFT JOIN categories ON models.category_id = categories.id
        """)

    rows = cur.fetchall()
    conn.close()

    models = []

    for row in rows:
        models.append(
            Model(
                id=row[0],
                name=row[1],
                modelNumber=row[2],
                category_id=row[3],
                category_name=row[4],
                description=row[5]
            )
        )

    return models


def insert(name, modelNumber, description, category_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO models (name, modelNumber, description, category_id)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        modelNumber,
        description,
        category_id,
    ))

    conn.commit()
    conn.close()


def update(model_id, name, modelNumber, description, category_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("UPDATE models SET name=? WHERE id=?",
                (name, model_id))

    conn.commit()
    conn.close()


def delete(asset_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM models WHERE id=?", (asset_id,))

    conn.commit()
    conn.close()
