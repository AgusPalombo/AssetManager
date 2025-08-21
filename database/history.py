from database.connection import get_connection
from datetime import datetime
from typing import Optional

def get_user_id_by_username(username: str) -> Optional[int]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario FROM usuarios WHERE nombre = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def log_historial(id_asset: Optional[int], id_usuario: int, descripcion: str):
    """Inserta un log global. id_asset puede ser None (ej. cambios de categorías)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO historial_cambios (id_asset, id_usuario, fecha_cambio, descripcion_cambio) VALUES (?, ?, ?, ?)",
        (id_asset, id_usuario, datetime.now().isoformat(timespec="seconds"), descripcion)
    )
    conn.commit()
    conn.close()
