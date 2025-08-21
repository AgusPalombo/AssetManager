import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from database.history import log_historial

def _edit_switch_details(self, id_asset: int):
    pop = tk.Toplevel(self.master)
    pop.title(f"Detalles · Switch (Asset #{id_asset})")
    pop.geometry("520x300")
    pop.resizable(False, False)

    tk.Label(pop, text="Cantidad de puertos:").pack(anchor="w", padx=10, pady=(8, 0))
    e_puertos = tk.Entry(pop, width=52); e_puertos.pack(padx=10)

    tk.Label(pop, text="Tipo (LAN o WiFi):").pack(anchor="w", padx=10, pady=(8, 0))
    e_tipo = tk.Entry(pop, width=52); e_tipo.pack(padx=10)

    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT cantidad_puertos, tipo FROM assets_switches WHERE id_asset=?", (id_asset,))
    row = cur.fetchone()
    if row:
        e_puertos.insert(0, "" if row[0] is None else str(row[0]))
        e_tipo.insert(0, row[1] or "")
    conn.close()

    def save():
        puertos_raw = e_puertos.get().strip()
        tipo = e_tipo.get().strip() or None
        puertos = None
        if puertos_raw:
            try:
                puertos = int(puertos_raw)
            except ValueError:
                messagebox.showerror("Error", "Cantidad de puertos debe ser un número entero.")
                return
        conn2 = get_connection(); c2 = conn2.cursor()
        c2.execute("SELECT 1 FROM assets_switches WHERE id_asset=?", (id_asset,))
        exists = c2.fetchone() is not None
        if exists:
            c2.execute("UPDATE assets_switches SET cantidad_puertos=?, tipo=? WHERE id_asset=?", (puertos, tipo, id_asset))
        else:
            c2.execute("INSERT INTO assets_switches (id_asset, cantidad_puertos, tipo) VALUES (?, ?, ?)", (id_asset, puertos, tipo))
        conn2.commit(); conn2.close()
        if self.current_user_id:
            log_historial(id_asset, self.current_user_id, "Actualización de detalles (Switch)")
        pop.destroy()
        self.load_activos()
        messagebox.showinfo("Éxito", "Detalles guardados.")

    tk.Button(pop, text="Guardar", width=16, height=2, command=save).pack(pady=12)