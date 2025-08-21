import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from database.history import log_historial

def _edit_access_point_details(self, id_asset: int):
    pop = tk.Toplevel(self.master)
    pop.title(f"Detalles · Access Point (Asset #{id_asset})")
    pop.geometry("520x360")
    pop.resizable(False, False)

    labels = ["IP", "MAC Address", "Usuario admin", "Contraseña admin"]
    entries = []
    for i, lbl in enumerate(labels):
        tk.Label(pop, text=lbl+":").pack(anchor="w", padx=10, pady=(8 if i==0 else 4, 0))
        show = "" if lbl != "Contraseña admin" else "*"  # si querés ocultar
        e = tk.Entry(pop, width=52, show=show)
        e.pack(padx=10)
        entries.append(e)

    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT ip, mac_address, usuario_admin, contrasena_admin FROM assets_access_points WHERE id_asset=?", (id_asset,))
    row = cur.fetchone()
    if row:
        for e, v in zip(entries, row):
            e.insert(0, "" if v is None else str(v))
    conn.close()

    def save():
        vals = [e.get().strip() or None for e in entries]
        conn2 = get_connection(); c2 = conn2.cursor()
        c2.execute("SELECT 1 FROM assets_access_points WHERE id_asset=?", (id_asset,))
        exists = c2.fetchone() is not None
        if exists:
            c2.execute("""
                UPDATE assets_access_points
                SET ip=?, mac_address=?, usuario_admin=?, contrasena_admin=?
                WHERE id_asset=?
            """, (*vals, id_asset))
        else:
            c2.execute("""
                INSERT INTO assets_access_points (id_asset, ip, mac_address, usuario_admin, contrasena_admin)
                VALUES (?, ?, ?, ?, ?)
            """, (id_asset, *vals))
        conn2.commit(); conn2.close()
        if self.current_user_id:
            log_historial(id_asset, self.current_user_id, "Actualización de detalles (Access Point)")
        pop.destroy()
        self.load_activos()
        messagebox.showinfo("Éxito", "Detalles guardados.")

    tk.Button(pop, text="Guardar", width=16, height=2, command=save).pack(pady=12)
