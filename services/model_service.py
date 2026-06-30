import sqlite3
from models.model import Model

DB_NAME = "assets.db"


def get_all(keyword="") -> list[Model]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    base_query = """
        SELECT 
            models.id, 
            models.name, 
            models.modelNumber, 
            categories.id, 
            categories.name, 
            models.description,
            manufacturers.id,
            manufacturers.name,
            COUNT(assets.id) as asset_count
        FROM models
        LEFT JOIN categories 
            ON models.category_id = categories.id
        LEFT JOIN manufacturers 
            ON models.manufacturer_id = manufacturers.id
        LEFT JOIN assets 
            ON assets.model_id = models.id
    """

    params = ()

    if keyword:
        base_query += """
            WHERE models.name LIKE ?
        """
        params = ('%' + keyword + '%',)

    base_query += """
        GROUP BY 
            models.id,
            models.name,
            models.modelNumber,
            categories.id,
            categories.name,
            models.description,
            manufacturers.id,
            manufacturers.name
    """

    cur.execute(base_query, params)

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
                description=row[5],
                manufacturer_id=row[6],
                manufacturer_name=row[7],
                asset_count=row[8],
            )
        )

    return models


def get_by_name(name):
    """Get asset by name"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM models WHERE name = ?", (name,))
    result = cur.fetchone()
    conn.close()
    return dict(result) if result else None


def insert(
    name,
    modelNumber,
    description,
    category_id,
    manufacturer_id
):
    # Validate uniqueness before insert
    if get_by_name(name):
        raise ValueError(f"Model with name '{name}' already exists")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO models (
            name, 
            modelNumber, 
            description, 
            category_id, 
            manufacturer_id
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        modelNumber,
        description,
        category_id,
        manufacturer_id,
    ))

    conn.commit()
    conn.close()


def update(
    model_id,
    name,
    modelNumber,
    description,
    category_id,
    manufacturer_id
):
    # When updating, exclude the current asset from uniqueness check
    existing_by_name = get_by_name(name)
    if existing_by_name and existing_by_name['id'] != category_id:
        raise ValueError(f"Model with name '{name}' already exists")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        UPDATE models SET 
            name=?, 
            modelNumber=?, 
            description=?, 
            category_id=?, 
            manufacturer_id=? 
        WHERE id=?
        """, (
        name,
        modelNumber,
        description,
        category_id,
        manufacturer_id,
        model_id
    ))

    conn.commit()
    conn.close()


def delete(asset_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM models WHERE id=?", (asset_id,))

    conn.commit()
    conn.close()


def count():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM models")

    total = cur.fetchone()[0]

    conn.close()

    return total
