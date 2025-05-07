# File no longer needed - using SQLite with table creation in user_repository.py
"""
CREATE TABLE IF NOT EXISTS users
(
    id            INTEGER PRIMARY KEY AUTO_INCREMENT,
    name          TEXT,
    family        TEXT,
    birthdate     TEXT,
    national_code TEXT,
    phone_number  TEXT,
    username      TEXT UNIQUE,
    password      TEXT
);

--

CREATE TABLE IF NOT EXISTS products
(
    id           INTEGER PRIMARY KEY AUTO_INCREMENT,
    category     TEXT,
    name         TEXT,
    company_name TEXT,
    price        REAL,
    quantity     INTEGER,
    exp_date     TEXT
);

--

#     user_id      INTEGER,
#     FOREIGN KEY (user_id) REFERENCES users (id)
"""