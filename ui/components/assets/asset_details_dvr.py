import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from database.history import log_historial

def _edit_dvr_details(self, id_asset: int):
    pop = tk.Toplevel(self.master)
    pop.title(f"Detalles · DVR (Asset #{id_asset})")
    pop.geometry("520x240")
    pop.resizable(False, False)

    tk.Label(pop, text="Cantidad de dispositivos conectados:").pack(anchor="w", padx=10, pady=(12, 0))
    e_cant = tk.Entry(pop, width=52); e_cant.pack(padx=10)

    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT cantidad_dispositivos_conectados FROM assets_dvrs WHERE id_asset=?", (id_asset,))
    row = cur.fetchone()
    if row:
        e_cant.insert(0, "" if row[0] is None else str(row[0]))
    conn.close()

    def save():
        raw = e_cant.get().strip()
        cant = None
        if raw:
            try:
                cant = int(raw)
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número entero.")
                return
        conn2 = get_connection(); c2 = conn2.cursor()
        c2.execute("SELECT 1 FROM assets_dvrs WHERE id_asset=?", (id_asset,))
        exists = c2.fetchone() is not None
        if exists:
            c2.execute("UPDATE assets_dvrs SET cantidad_dispositivos_conectados=? WHERE id_asset=?", (cant, id_asset))
        else:
            c2.execute("INSERT INTO assets_dvrs (id_asset, cantidad_dispositivos_conectados) VALUES (?, ?)", (id_asset, cant))
        conn2.commit(); conn2.close()
        if self.current_user_id:
            log_historial(id_asset, self.current_user_id, "Actualización de detalles (DVR)")
        pop.destroy()
        self.load_activos()
        messagebox.showinfo("Éxito", "Detalles guardados.")

    tk.Button(pop, text="Guardar", width=16, height=2, command=save).pack(pady=12)