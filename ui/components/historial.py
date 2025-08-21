import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import get_connection

class HistorialWindow:
    def __init__(self, master, id_asset: int):
        self.master = master
        self.id_asset = id_asset
        master.title(f"Historial de Cambios · Asset #{id_asset}")
        master.geometry("760x380")
        master.resizable(False, False)

        # Tabla
        self.tree = ttk.Treeview(master, columns=("fecha","usuario","descripcion"), show="headings")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.column("fecha", width=160, anchor="w")
        self.tree.column("usuario", width=160, anchor="w")
        self.tree.column("descripcion", width=410, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=10)

        # Botones
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refrescar", width=16, height=2, command=self.load_data).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Cerrar", width=16, height=2, command=master.destroy).grid(row=0, column=1, padx=6)

        self.load_data()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT h.fecha_cambio, u.nombre AS usuario, h.descripcion_cambio
            FROM historial_cambios h
            LEFT JOIN usuarios u ON u.id_usuario = h.id_usuario
            WHERE h.id_asset = ?
            ORDER BY h.id_historial DESC
        """, (self.id_asset,))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Historial", "No hay registros de cambios para este activo.")

        for fecha, usuario, desc in rows:
            self.tree.insert("", tk.END, values=(fecha, usuario or "-", desc))