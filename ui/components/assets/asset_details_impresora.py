import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from database.history import log_historial

class ImpresoraDetails:
    def __init__(self, master, id_asset: int, current_user_id: int):
        self.master = master
        self.id_asset = id_asset
        self.current_user_id = current_user_id

        master.title(f"Detalles de Impresora · Asset #{id_asset}")
        master.geometry("460x360")
        master.resizable(False, False)

        wrap = tk.Frame(master, padx=12, pady=12)
        wrap.pack(fill="both", expand=True)

        self.e_marca = self._field(wrap, "Marca:")
        self.e_modelo = self._field(wrap, "Modelo:")
        self.e_nro = self._field(wrap, "Nro. Serie:")
        self.e_ip = self._field(wrap, "IP:")

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
            SELECT marca, modelo, nro_serie, ip FROM assets_impresoras WHERE id_asset=?
        """, (self.id_asset,))
        row = cur.fetchone()
        conn.close()
        if row:
            vals = ["" if v is None else str(v) for v in row]
            self.e_marca.insert(0, vals[0])
            self.e_modelo.insert(0, vals[1])
            self.e_nro.insert(0, vals[2])
            self.e_ip.insert(0, vals[3])

    def _save(self):
        marca = self.e_marca.get().strip()
        modelo = self.e_modelo.get().strip()
        nro = self.e_nro.get().strip()
        ip = self.e_ip.get().strip()

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE assets_impresoras SET marca=?, modelo=?, nro_serie=?, ip=? WHERE id_asset=?
        """, (marca, modelo, nro, ip, self.id_asset))
        if cur.rowcount == 0:
            cur.execute("""
                INSERT INTO assets_impresoras (id_asset, marca, modelo, nro_serie, ip)
                VALUES (?, ?, ?, ?, ?)
            """, (self.id_asset, marca, modelo, nro, ip))
        conn.commit()
        conn.close()

        if self.current_user_id:
            log_historial(self.id_asset, self.current_user_id, "Actualización detalles de impresora")
        messagebox.showinfo("Éxito", "Detalles de impresora guardados.")
        self.master.destroy()