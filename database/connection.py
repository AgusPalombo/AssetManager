import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent.parent / "data.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    # Habilitar claves foráneas en SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn