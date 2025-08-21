import bcrypt
from database.connection import get_connection

def list_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nombre, rol, activo FROM usuarios ORDER BY id_usuario")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_user_by_name(nombre: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nombre, rol, activo FROM usuarios WHERE nombre = ?", (nombre,))
    row = cur.fetchone()
    conn.close()
    return row

def count_admins():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM usuarios WHERE rol='admin' AND activo=1")
    n = cur.fetchone()[0]
    conn.close()
    return n

def create_user(nombre: str, password_plain: str, rol: str):
    hashed = bcrypt.hashpw(password_plain.encode("utf-8"), bcrypt.gensalt())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nombre, password_hash, rol, activo) VALUES (?, ?, ?, 1)",
                (nombre, hashed, rol))
    conn.commit()
    uid = cur.lastrowid
    conn.close()
    return uid

def update_user(user_id: int, nombre: str, rol: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET nombre=?, rol=? WHERE id_usuario=?",
                (nombre, rol, user_id))
    conn.commit()
    conn.close()

def reset_password(user_id: int, new_password: str):
    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET password_hash=? WHERE id_usuario=?",
                (hashed, user_id))
    conn.commit()
    conn.close()

def set_active(user_id: int, active: bool):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE usuarios SET activo=? WHERE id_usuario=?", (1 if active else 0, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id_usuario=?", (user_id,))
    conn.commit()
    conn.close()