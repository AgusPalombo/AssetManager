import bcrypt
from database.connection import get_connection

def create_admin_user():
    conn = get_connection()
    cursor = conn.cursor()

    nombre_admin = "admin"
    password_admin = "admin123"
    hashed = bcrypt.hashpw(password_admin.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            INSERT INTO usuarios (nombre, password_hash, rol)
            VALUES (?, ?, ?)
        """, (nombre_admin, hashed, "admin"))
        conn.commit()
        print("✅ Usuario admin creado con éxito.")
    except Exception:
        print("ℹ️ Usuario admin ya existe.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_admin_user()
