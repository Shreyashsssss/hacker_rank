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
