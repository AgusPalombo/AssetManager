import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from database.history import log_historial

class ComputadoraDetails:
    def __init__(self, master, id_asset: int, current_user_id: int):
        self.master = master
        self.id_asset = id_asset
        self.current_user_id = current_user_id

        master.title(f"Detalles de Computadora · Asset #{id_asset}")
        master.geometry("460x420")
        master.resizable(False, False)

        wrap = tk.Frame(master, padx=12, pady=12)
        wrap.pack(fill="both", expand=True)

        # Campos
        self.e_ip = self._field(wrap, "IP:")
        self.e_mother = self._field(wrap, "Motherboard:")
        self.e_cpu = self._field(wrap, "Procesador:")
        self.e_ram_tipo = self._field(wrap, "RAM Tipo:")
        self.e_ram_cant = self._field(wrap, "RAM Cantidad (GB):")
        self.e_ssd = self._field(wrap, "SSD (ej. 512GB):")
        self.e_hdd = self._field(wrap, "HDD (ej. 1TB):")
        self.e_nic = self._field(wrap, "Placa red externa:")

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
            SELECT ip, motherboard, procesador, ram_tipo, ram_cantidad, ssd, hdd, placa_red_ext
            FROM assets_computadoras WHERE id_asset=?
        """, (self.id_asset,))
        row = cur.fetchone()
        conn.close()
        if row:
            vals = ["" if v is None else str(v) for v in row]
            self.e_ip.insert(0, vals[0])
            self.e_mother.insert(0, vals[1])
            self.e_cpu.insert(0, vals[2])
            self.e_ram_tipo.insert(0, vals[3])
            self.e_ram_cant.insert(0, vals[4])
            self.e_ssd.insert(0, vals[5])
            self.e_hdd.insert(0, vals[6])
            self.e_nic.insert(0, vals[7])

    def _save(self):
        ip = self.e_ip.get().strip()
        mother = self.e_mother.get().strip()
        cpu = self.e_cpu.get().strip()
        ram_tipo = self.e_ram_tipo.get().strip()
        ram_cant = self.e_ram_cant.get().strip()
        ssd = self.e_ssd.get().strip()
        hdd = self.e_hdd.get().strip()
        nic = self.e_nic.get().strip()

        conn = get_connection()
        cur = conn.cursor()
        # upsert manual: intentar update, si no afectó filas -> insert
        cur.execute("""
            UPDATE assets_computadoras
            SET ip=?, motherboard=?, procesador=?, ram_tipo=?, ram_cantidad=?, ssd=?, hdd=?, placa_red_ext=?
            WHERE id_asset=?
        """, (ip, mother, cpu, ram_tipo, int(ram_cant) if ram_cant.isdigit() else None, ssd, hdd, nic, self.id_asset))
        if cur.rowcount == 0:
            cur.execute("""
                INSERT INTO assets_computadoras
                (id_asset, ip, motherboard, procesador, ram_tipo, ram_cantidad, ssd, hdd, placa_red_ext)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.id_asset, ip, mother, cpu, ram_tipo, int(ram_cant) if ram_cant.isdigit() else None, ssd, hdd, nic))
        conn.commit()
        conn.close()

        if self.current_user_id:
            log_historial(self.id_asset, self.current_user_id, "Actualización detalles de computadora")
        messagebox.showinfo("Éxito", "Detalles de computadora guardados.")
        self.master.destroy()