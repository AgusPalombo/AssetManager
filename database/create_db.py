from database.connection import get_connection

def _ensure_column_activo():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(usuarios);")
    cols = [r[1] for r in cur.fetchall()]
    if "activo" not in cols:
        cur.execute("ALTER TABLE usuarios ADD COLUMN activo INTEGER DEFAULT 1")
        conn.commit()
    conn.close()

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla de categorias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias_asset (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        descripcion TEXT
    )
    """)

    
    # Tabla de usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('admin','usuario')),
        activo INTEGER DEFAULT 1
    )
    """)

    
    # Tabla de assets genérica
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id_asset INTEGER PRIMARY KEY AUTOINCREMENT,
        id_categoria INTEGER NOT NULL,
        nombre TEXT NOT NULL,
        identificador TEXT,
        fecha_alta TEXT,
        fecha_baja TEXT,
        ubicacion TEXT,
        observaciones TEXT,
        FOREIGN KEY (id_categoria) REFERENCES categorias_asset(id_categoria)
    )
    """)

    # Tablas específicas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets_computadoras (
        id_asset INTEGER PRIMARY KEY,
        ip TEXT,
        motherboard TEXT,
        procesador TEXT,
        ram_tipo TEXT,
        ram_cantidad INTEGER,
        ssd TEXT,
        hdd TEXT,
        placa_red_ext TEXT,
        FOREIGN KEY (id_asset) REFERENCES assets(id_asset)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets_impresoras (
        id_asset INTEGER PRIMARY KEY,
        marca TEXT,
        modelo TEXT,
        nro_serie TEXT,
        ip TEXT,
        FOREIGN KEY (id_asset) REFERENCES assets(id_asset)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets_perifericos (
        id_asset INTEGER PRIMARY KEY,
        tipo TEXT,
        marca TEXT,
        fecha_registro TEXT,
        fecha_entrega TEXT,
        FOREIGN KEY (id_asset) REFERENCES assets(id_asset)
    )
    """)

    # Historial de cambios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_cambios (
        id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
        id_asset INTEGER,
        id_usuario INTEGER,
        fecha_cambio TEXT,
        descripcion_cambio TEXT,
        FOREIGN KEY (id_asset) REFERENCES assets(id_asset) ON DELETE SET NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE NO ACTION
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    create_tables()