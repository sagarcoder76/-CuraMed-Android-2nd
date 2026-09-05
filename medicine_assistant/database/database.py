"""
database.py
-----------
Everything about the local SQLite database lives here:

  * get_connection()        -> open a connection to the .db file
  * initialize_database()   -> create the `medicines` table (safe to re-run)
  * insert_medicine()       -> add one medicine row
  * fetch_all_medicines()   -> read every row as Medicine objects
  * count_medicines()       -> how many rows exist

Privacy note: SQLite is a single local file on the user's own computer.
Nothing is sent anywhere — there is no server and no internet involved.
"""

import sqlite3
from pathlib import Path
from typing import List

from .models import Medicine

# The database file lives inside the `database/` folder, next to this file.
DB_PATH = Path(__file__).resolve().parent / "medicine_database.db"

# ---------------------------------------------------------------------------
# Table schema — mirrors the fields requested in the project specification.
# ---------------------------------------------------------------------------
CREATE_MEDICINES_TABLE = """
CREATE TABLE IF NOT EXISTS medicines (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name         TEXT NOT NULL,
    brand_name            TEXT,
    generic_name          TEXT,
    active_ingredient     TEXT,
    strength              TEXT,
    category              TEXT,
    common_uses           TEXT,
    general_usage         TEXT,
    administration        TEXT,
    common_side_effects   TEXT,
    serious_warnings      TEXT,
    pregnancy_warning     TEXT,
    breastfeeding_warning TEXT,
    children_warning      TEXT,
    elderly_warning       TEXT,
    kidney_warning        TEXT,
    liver_warning         TEXT,
    drug_interactions     TEXT,
    food_interactions     TEXT,
    storage_information   TEXT,
    manufacturer          TEXT,
    dosage_form           TEXT,
    source                TEXT,
    last_updated          TEXT
);
"""

# Index speeds up name lookups once the database grows.
CREATE_NAME_INDEX = """
CREATE INDEX IF NOT EXISTS idx_medicines_name ON medicines (medicine_name);
"""

# Ordered list of insertable columns (everything except the auto `id`).
MEDICINE_COLUMNS = [
    "medicine_name", "brand_name", "generic_name", "active_ingredient",
    "strength", "category", "common_uses", "general_usage", "administration",
    "common_side_effects", "serious_warnings", "pregnancy_warning",
    "breastfeeding_warning", "children_warning", "elderly_warning",
    "kidney_warning", "liver_warning", "drug_interactions",
    "food_interactions", "storage_information", "manufacturer",
    "dosage_form", "source", "last_updated",
]


def get_connection(db_path=None) -> sqlite3.Connection:
    """
    Open (and create if needed) the SQLite database file.

    `row_factory = sqlite3.Row` lets us access columns by name, which
    `Medicine.from_row()` relies on.
    """
    path = Path(db_path) if db_path else DB_PATH
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    """Create the table and index if they do not exist yet. Safe to re-run."""
    cursor = connection.cursor()
    cursor.execute(CREATE_MEDICINES_TABLE)
    cursor.execute(CREATE_NAME_INDEX)
    connection.commit()


def insert_medicine(connection: sqlite3.Connection, data: dict) -> int:
    """
    Insert one medicine described by `data` (a dict of column -> value).

    Uses parameter placeholders (?) so values are never glued into SQL —
    this prevents SQL injection even if data comes from an untrusted file.
    Returns the new row's id.
    """
    # Keep only columns the table actually has; missing ones become None.
    safe_data = {column: data.get(column) for column in MEDICINE_COLUMNS}
    placeholders = ", ".join("?" for _ in MEDICINE_COLUMNS)
    sql = (
        f"INSERT INTO medicines ({', '.join(MEDICINE_COLUMNS)}) "
        f"VALUES ({placeholders})"
    )
    cursor = connection.cursor()
    cursor.execute(sql, [safe_data[column] for column in MEDICINE_COLUMNS])
    connection.commit()
    return cursor.lastrowid


def fetch_all_medicines(connection: sqlite3.Connection) -> List[Medicine]:
    """Return every medicine in the database as Medicine objects (A–Z)."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM medicines ORDER BY medicine_name COLLATE NOCASE")
    return [Medicine.from_row(row) for row in cursor.fetchall()]


def count_medicines(connection: sqlite3.Connection) -> int:
    """Return how many medicine rows exist."""
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM medicines")
    return cursor.fetchone()[0]
