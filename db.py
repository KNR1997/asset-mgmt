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

    # Manufacturers
    cur.execute("""
    CREATE TABLE IF NOT EXISTS manufacturers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        url TEXT,
        supportURL TEXT,
        supportPhone TEXT,
        warrantyLookupUrl TEXT,
        supportEmail TEXT,
        notes TEXT
    )
    """)

    # Types
    cur.execute("""
    CREATE TABLE IF NOT EXISTS types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    # Default types
    cur.execute("""
    INSERT OR IGNORE INTO types (name)
    VALUES
        ('Asset'),
        ('License'),
        ('Accessory'),
        ('Consumable')
    """)

    # Categories
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        type_id INTEGER,
        FOREIGN KEY (type_id) REFERENCES types(id)
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
        manufacturer_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id),
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
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

    # Accessories
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accessories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        accessoryName TEXT NOT NULL,
        categoryName TEXT NOT NULL,
        supplierName TEXT,
        modelNumber TEXT,
        minQuantity INTEGER,
        orderNumber TEXT,
        unitCost INTEGER,
        purchaseDate TEXT,
        qunatity INTEGER,
        notes TEXT,     
        manufacturer_id INTEGER,
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
    )
    """)

    # Licenses
    cur.execute("""
    CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        softwareName TEXT NOT NULL,
        categoryName TEXT NOT NULL,
        seats INTEGER DEFAULT 0,
        minQuantity INTEGER,
        productKey TEXT,
        licensedTo TEXT,
        licensedToEmail TEXT,
        orderNumber TEXT,
        purchaseCost INTEGER,
        purchaseDate TEXT,
        expirationDate TEXT,
        terminationDate TEXT,
        notes TEXT,     
        manufacturer_id INTEGER,
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
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

    # Repairs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS repairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_id INTEGER NOT NULL,
        checkout_id INTEGER,  -- Optional: link to the checkout that caused the damage
        repair_date TEXT NOT NULL,
        repair_cost REAL,
        status TEXT DEFAULT 'Completed',  -- 'Pending', 'In Progress', 'Completed'
        description TEXT,
        notes TEXT,
        performed_by TEXT,  -- Repair technician or company name
        warranty_covered BOOLEAN DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE,
        FOREIGN KEY (checkout_id) REFERENCES checkouts(id) ON DELETE SET NULL
    )
    """)
    
    conn.commit()
    conn.close()
