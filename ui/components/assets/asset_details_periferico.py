import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from database.history import log_historial

class PerifericoDetails:
    def __init__(self, master, id_asset: int, current_user_id: int):
        self.master = master
        self.id_asset = id_asset
        self.current_user_id = current_user_id

        master.title(f"Detalles de Periférico · Asset #{id_asset}")
        master.geometry("460x360")
        master.resizable(False, False)

        wrap = tk.Frame(master, padx=12, pady=12)
        wrap.pack(fill="both", expand=True)

        self.e_tipo = self._field(wrap, "Tipo (ej. mouse/teclado):")
        self.e_marca = self._field(wrap, "Marca:")
        self.e_reg = self._field(wrap, "Fecha registro (YYYY-MM-DD):")
        self.e_ent = self._field(wrap, "Fecha entrega (YYYY-MM-DD):")

        self._load_existing()

        tk.Button(wrap, text="Guardar", width=18, height=2, command=self._save).pack(pady=10)

    def _field(self, parent, label):
        tk.Label(parent, text=label).pack(anchor="w")
        e = tk.Entry(parent, width=50)
        e.pack(pady=(0,8))
        return e

    def _load_existing(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT tipo, marca, fecha_registro, fecha_entrega FROM assets_perifericos WHERE id_asset=?
        """, (self.id_asset,))
        row = cur.fetchone()
        conn.close()
        if row:
            vals = ["" if v is None else str(v) for v in row]
            self.e_tipo.insert(0, vals[0])
            self.e_marca.insert(0, vals[1])
            self.e_reg.insert(0, vals[2])
            self.e_ent.insert(0, vals[3])

    def _save(self):
        tipo = self.e_tipo.get().strip()
        marca = self.e_marca.get().strip()
        f_reg = self.e_reg.get().strip() or None
        f_ent = self.e_ent.get().strip() or None

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE assets_perifericos SET tipo=?, marca=?, fecha_registro=?, fecha_entrega=? WHERE id_asset=?
        """, (tipo, marca, f_reg, f_ent, self.id_asset))
        if cur.rowcount == 0:
            cur.execute("""
                INSERT INTO assets_perifericos (id_asset, tipo, marca, fecha_registro, fecha_entrega)
                VALUES (?, ?, ?, ?, ?)
            """, (self.id_asset, tipo, marca, f_reg, f_ent))
        conn.commit()
        conn.close()

        if self.current_user_id:
            log_historial(self.id_asset, self.current_user_id, "Actualización detalles de periférico")
        messagebox.showinfo("Éxito", "Detalles de periférico guardados.")
        self.master.destroy()