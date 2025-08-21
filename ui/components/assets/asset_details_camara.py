import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from database.history import log_historial

def _edit_camara_details(self, id_asset: int):
    pop = tk.Toplevel(self.master)
    pop.title(f"Detalles · Cámara (Asset #{id_asset})")
    pop.geometry("520x420")
    pop.resizable(False, False)

    fields = [("Marca",""), ("Modelo",""), ("Tipo",""), ("Patrón utilizado","")]
    entries = []
    for i, (lbl, _) in enumerate(fields):
        tk.Label(pop, text=lbl+":").pack(anchor="w", padx=10, pady=(8 if i==0 else 4, 0))
        # Para “Patrón utilizado” usamos Text largo:
        if lbl == "Patrón utilizado":
            txt = tk.Text(pop, width=52, height=6); txt.pack(padx=10); entries.append(txt)
        else:
            e = tk.Entry(pop, width=52); e.pack(padx=10); entries.append(e)

    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT marca, modelo, tipo, patron_utilizado FROM assets_camaras WHERE id_asset=?", (id_asset,))
    row = cur.fetchone()
    if row:
        # marca, modelo, tipo, patron
        for i, v in enumerate(row):
            if i < 3:
                entries[i].insert(0, "" if v is None else str(v))
            else:
                entries[i].insert("1.0", "" if v is None else str(v))
    conn.close()

    def save():
        marca = entries[0].get().strip() or None
        modelo = entries[1].get().strip() or None
        tipo = entries[2].get().strip() or None
        patron = entries[3].get("1.0", "end").strip() or None

        conn2 = get_connection(); c2 = conn2.cursor()
        c2.execute("SELECT 1 FROM assets_camaras WHERE id_asset=?", (id_asset,))
        exists = c2.fetchone() is not None
        if exists:
            c2.execute("""
                UPDATE assets_camaras
                SET marca=?, modelo=?, tipo=?, patron_utilizado=?
                WHERE id_asset=?
            """, (marca, modelo, tipo, patron, id_asset))
        else:
            c2.execute("""
                INSERT INTO assets_camaras (id_asset, marca, modelo, tipo, patron_utilizado)
                VALUES (?, ?, ?, ?, ?)
            """, (id_asset, marca, modelo, tipo, patron))
        conn2.commit(); conn2.close()
        if self.current_user_id:
            log_historial(id_asset, self.current_user_id, "Actualización de detalles (Cámara)")
        pop.destroy()
        self.load_activos()
        messagebox.showinfo("Éxito", "Detalles guardados.")

    tk.Button(pop, text="Guardar", width=16, height=2, command=save).pack(pady=12)