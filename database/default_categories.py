# database/init_db.py
from database.connection import get_connection

def seed_default_categories():
    """
    Inserta categorías base si no existen:
      - Computadora
      - Impresora
      - Periférico
    Usa un índice único por nombre para evitar duplicados.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Índice único por nombre para poder INSERT OR IGNORE
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_categorias_nombre
        ON categorias_asset(nombre)
    """)

    categorias = [
        (
            "Computadora",
            "Activos de computo (desktop/notebook). Detalles esperados: "
            "ip, motherboard, procesador, ram_tipo, ram_cantidad, ssd, hdd, placa_red_ext."
        ),
        (
            "Impresora",
            "Equipos de impresion. Detalles esperados: marca, modelo, nro_serie, ip."
        ),
        (
            "Periferico",
            "Perifericos (teclado, mouse, audífonos, etc.). Detalles esperados: "
            "tipo, marca, fecha_registro, fecha_entrega."
        ),
        (
            "Access Point",
            "Puntos de acceso de red. Detalles: ip, mac_address, usuario_admin, contrasena_admin."
        ),
        (
            "Switch",
            "Conmutadores de red. Detalles: cantidad_puertos, tipo (LAN o WiFi)."
        ),
        (
            "Camara",
            "Cámaras de seguridad. Detalles: marca, modelo, tipo, patron_utilizado."
        ),
        (
            "DVR",
            "Grabadores de video digital. Detalles: cantidad_dispositivos_conectados."
        ),
    ]



    for nombre, descripcion in categorias:
        cur.execute(
            "INSERT OR IGNORE INTO categorias_asset (nombre, descripcion) VALUES (?, ?)",
            (nombre, descripcion)
        )

    conn.commit()
    conn.close()
