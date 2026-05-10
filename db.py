import sqlite3


def connect():
    conn = sqlite3.connect("assets.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def setup():
    conn = connect()
    cur = conn.cursor()

    # Admin table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # Employees
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT
    )
    """)

    # Categories
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT
    )
    """)

    # Models
    cur.execute("""
    CREATE TABLE IF NOT EXISTS models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        modelNumber TEXT,
        description TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    """)

    # Assets
    cur.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        tag TEXT UNIQUE NOT NULL,
        serialNumber TEXT UNIQUE,
        description TEXT,
        status TEXT,
        purchaseDate TEXT,
        purchaseCost REAL,
        model_id INTEGER,
        FOREIGN KEY (model_id) REFERENCES models(id)
    )
    """)

    # Checkout
    cur.execute("""
    CREATE TABLE IF NOT EXISTS checkouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        asset_id INTEGER NOT NULL,
        employee_id INTEGER NOT NULL,

        checkout_date TEXT NOT NULL,
        expected_checkin_date TEXT,

        actual_checkin_date TEXT,

        is_active INTEGER NOT NULL DEFAULT 1,

        return_condition TEXT,

        checkout_notes TEXT,
        return_notes TEXT,

        created_at TEXT DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (asset_id) REFERENCES assets(id),
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    """)

    conn.commit()
    conn.close()
