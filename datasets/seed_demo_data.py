import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("demo_ecommerce.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript(
    """
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS payments;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        signup_date TEXT
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        paid_at TEXT,
        cancelled_at TEXT,
        amount REAL,
        status TEXT
    );

    CREATE TABLE order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        sku TEXT,
        qty INTEGER,
        unit_price REAL
    );

    CREATE TABLE payments (
        payment_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        paid_at TEXT,
        status TEXT
    );
    """
)

cur.executemany(
    "INSERT INTO customers (customer_id, name, signup_date) VALUES (?, ?, ?)",
    [
        (1, "Ada", "2024-01-11"),
        (2, "Ben", "2024-02-02"),
        (3, "Cara", "2024-03-15"),
        (4, "Drew", "2024-04-20"),
    ],
)

cur.executemany(
    "INSERT INTO orders (order_id, customer_id, order_date, paid_at, cancelled_at, amount, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
    [
        (101, 1, "2025-06-15T10:00:00", "2025-06-16T12:00:00", None, 80.00, "paid"),
        (102, 2, "2025-06-30T12:00:00", "2025-06-30T18:00:00", None, 120.00, "paid"),
        (103, 2, "2025-07-01T00:00:00", "2025-07-01T00:00:00", None, 150.00, "paid"),
        (104, 3, "2025-06-20T08:00:00", None, "2025-06-21T08:00:00", 60.00, "cancelled"),
        (105, 4, "2025-06-25T00:00:00", None, None, 0.00, "pending"),
    ],
)

cur.executemany(
    "INSERT INTO order_items (item_id, order_id, sku, qty, unit_price) VALUES (?, ?, ?, ?, ?)",
    [
        (1, 101, "A1", 2, 40.00),
        (2, 102, "B2", 1, 120.00),
        (3, 103, "C3", 1, 150.00),
        (4, 104, "D4", 1, 60.00),
    ],
)

cur.executemany(
    "INSERT INTO payments (payment_id, customer_id, amount, paid_at, status) VALUES (?, ?, ?, ?, ?)",
    [
        (1, 1, 80.00, "2025-06-16T12:00:00", "paid"),
        (2, 2, 120.00, "2025-06-30T18:00:00", "paid"),
        (3, 2, 160.00, "2025-07-01T00:00:00", "paid"),
        (4, 3, 60.00, "2025-06-25T00:00:00", "paid"),
    ],
)

conn.commit()
conn.close()
print(f"Created demo database at {DB_PATH}")
