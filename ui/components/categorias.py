import tkinter as tk
from tkinter import messagebox
from database.connection import get_connection
from ui.components.ui_theme import FONT_LABEL, FONT_TITLE, BTN_KW

class CategoriasWindow:
    def __init__(self, master, current_username=None, current_role="admin", **_):
        self.master = master
        self.current_username = current_username
        self.current_role = current_role

        master.title("Gestión de Categorías")
        master.geometry("800x600")
        master.resizable(False, False)

        list_font = ("Segoe UI", 12)

        # Wrapper con padding
        wrap = tk.Frame(master, padx=12, pady=12)
        wrap.pack(fill="both", expand=True)

        # Título
        tk.Label(wrap, text="Categorías de Activos", font=FONT_TITLE).pack(pady=(0, 10), anchor="w")

        # Listbox con scrollbar
        list_frame = tk.Frame(wrap)
        list_frame.pack(fill="both", expand=True, pady=(0, 8))

        self.listbox = tk.Listbox(list_frame, width=60, height=14, font=list_font)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Botonera grande
        btns = tk.Frame(wrap)
        btns.pack(fill="x", pady=(6, 0))

        self.btn_add = tk.Button(btns, text="Agregar", command=self.add_categoria, **BTN_KW)
        self.btn_add.pack(side="left", padx=4, expand=True, fill="x")

        self.btn_edit = tk.Button(btns, text="Modificar", command=self.edit_categoria, **BTN_KW)
        self.btn_edit.pack(side="left", padx=4, expand=True, fill="x")

        self.btn_delete = tk.Button(btns, text="Eliminar", command=self.delete_categoria, **BTN_KW)
        self.btn_delete.pack(side="left", padx=4, expand=True, fill="x")

        self.btn_refresh = tk.Button(btns, text="Refrescar", command=self.load_categorias, **BTN_KW)
        self.btn_refresh.pack(side="left", padx=4, expand=True, fill="x")

        # Cargar categorías al iniciar
        self.load_categorias()

        # ---- Permisos: modo solo lectura si no es admin ----
        if self.current_role != "admin":
            self.btn_add.destroy()
            self.btn_edit.destroy()
            self.btn_delete.destroy()

    # ----------------- Data -----------------
    def load_categorias(self):
        """Carga todas las categorías desde la DB y las muestra en el Listbox"""
        self.listbox.delete(0, tk.END)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_categoria, nombre FROM categorias_asset ORDER BY id_categoria")
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            self.listbox.insert(tk.END, f"{row[0]} - {row[1]}")

    def _get_selected_categoria(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una categoría.")
            return None
        item = self.listbox.get(sel[0])
        id_categoria = int(item.split(" - ")[0])
        return id_categoria

    # ----------------- Alta -----------------
    def add_categoria(self):
        """Popup para agregar una categoría (solo admin)"""
        if self.current_role != "admin":
            messagebox.showerror("Permisos", "No tenés permisos para agregar categorías.")
            return

        popup = tk.Toplevel(self.master)
        popup.title("Nueva Categoría")
        popup.geometry("420x280")
        popup.resizable(False, False)

        wrap = tk.Frame(popup, padx=12, pady=12)
        wrap.pack(fill="both", expand=True)

        tk.Label(wrap, text="Nombre:", font=FONT_LABEL).pack(anchor="w")
        entry_nombre = tk.Entry(wrap, width=44)
        entry_nombre.pack(pady=(0, 8))

        tk.Label(wrap, text="Descripción:", font=FONT_LABEL).pack(anchor="w")
        entry_desc = tk.Text(wrap, width=44, height=7)
        entry_desc.pack()

        def save_categoria():
            nombre = entry_nombre.get().strip()
            descripcion = entry_desc.get("1.0", tk.END).strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio.")
                return

            conn = get_connection()
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO categorias_asset (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
                conn.commit()
                messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
                popup.destroy()
                self.load_categorias()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la categoría: {e}")
            finally:
                conn.close()

        tk.Button(wrap, text="Guardar", command=save_categoria, **BTN_KW).pack(pady=10, fill="x")
        entry_nombre.focus_set()

    # ----------------- Modificación -----------------
    def edit_categoria(self):
        """Modificar nombre/descr. de la categoría seleccionada (solo admin)"""
        if self.current_role != "admin":
            messagebox.showerror("Permisos", "No tenés permisos para modificar categorías.")
            return

        id_categoria = self._get_selected_categoria()
        if id_categoria is None:
            return

        # Traer datos actuales
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT nombre, descripcion FROM categorias_asset WHERE id_categoria = ?", (id_categoria,))
        row = cur.fetchone()
        conn.close()
        if not row:
            messagebox.showerror("Error", "No se encontró la categoría.")
            return
        nombre_actual, desc_actual = row[0] or "", row[1] or ""

        # Popup edición
        popup = tk.Toplevel(self.master)
        popup.title(f"Modificar Categoría #{id_categoria}")
        popup.geometry("420x300")
        popup.resizable(False, False)

        wrap = tk.Frame(popup, padx=12, pady=12)
        wrap.pack(fill="both", expand=True)

        tk.Label(wrap, text="Nombre:", font=FONT_LABEL).pack(anchor="w")
        entry_nombre = tk.Entry(wrap, width=44)
        entry_nombre.insert(0, nombre_actual)
        entry_nombre.pack(pady=(0, 8))

        tk.Label(wrap, text="Descripción:", font=FONT_LABEL).pack(anchor="w")
        entry_desc = tk.Text(wrap, width=44, height=8)
        entry_desc.insert("1.0", desc_actual)
        entry_desc.pack()

        def save_changes():
            new_nombre = entry_nombre.get().strip()
            new_desc = entry_desc.get("1.0", tk.END).strip()

            if not new_nombre:
                messagebox.showerror("Error", "El nombre es obligatorio.")
                return

            conn2 = get_connection()
            cur2 = conn2.cursor()
            try:
                cur2.execute("""
                    UPDATE categorias_asset
                    SET nombre = ?, descripcion = ?
                    WHERE id_categoria = ?
                """, (new_nombre, new_desc, id_categoria))
                conn2.commit()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la categoría: {e}")
                conn2.close()
                return
            conn2.close()

            # Aviso
            messagebox.showinfo(
                "Éxito",
                "Categoría actualizada.\n\n"
                "Los activos que pertenecen a esta categoría verán el nuevo nombre "
                "automáticamente en las pantallas y exportaciones."
            )
            popup.destroy()
            self.load_categorias()

        tk.Button(wrap, text="Guardar cambios", command=save_changes, **BTN_KW).pack(pady=10, fill="x")

    # ----------------- Baja -----------------
    def delete_categoria(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccioná una categoría para eliminar.")
            return

        item = self.listbox.get(sel[0])  # "id - nombre"
        try:
            id_categoria = int(item.split(" - ")[0])
            nombre = item.split(" - ", 1)[1]
        except Exception:
            messagebox.showerror("Error", "No se pudo obtener la categoría seleccionada.")
            return

        nombre_lower = (nombre or "").strip().lower()

        # Categorías protegidas (con y sin tilde)
        core_cats = ("computadora", "impresora", "periférico", "periferico", "Access Point","Switch", "Camara", "DVR")
        if any(c in nombre_lower for c in core_cats):
            messagebox.showerror("Bloqueado", f"La categoría '{nombre}' es base del sistema y no puede eliminarse.")
            return

        # ¿Tiene assets asociados?
        conn = get_connection(); cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM assets WHERE id_categoria = ?", (id_categoria,))
            activos_count = cur.fetchone()[0]
        except Exception as e:
            conn.close()
            messagebox.showerror("Error", f"No se pudo verificar activos asociados: {e}")
            return

        if activos_count > 0:
            # --- Popup de reasignación ---
            conn.close()  # cerramos esta conexión; el popup usará una nueva
            popup = tk.Toplevel(self.master)
            popup.title("Reasignar Activos")
            popup.geometry("460x220")
            popup.transient(self.master)
            popup.grab_set()

            wrap = tk.Frame(popup, padx=12, pady=12)
            wrap.pack(fill="both", expand=True)

            tk.Label(
                wrap,
                text=(f"La categoría '{nombre}' tiene {activos_count} activo(s).\n"
                    "Seleccioná otra categoría para reasignarlos y poder eliminarla."),
                justify="left"
            ).pack(anchor="w", pady=(0,10))

            # Cargar categorías destino (todas menos la actual)
            conn2 = get_connection(); c2 = conn2.cursor()
            c2.execute("""
                SELECT id_categoria, nombre
                FROM categorias_asset
                WHERE id_categoria <> ?
                ORDER BY nombre
            """, (id_categoria,))
            destinos = c2.fetchall()
            conn2.close()

            if not destinos:
                tk.Label(wrap, text="No hay categorías disponibles para reasignar.", fg="red").pack(anchor="w", pady=8)
                tk.Button(wrap, text="Cerrar", command=popup.destroy, **BTN_KW).pack(pady=(14,0), fill="x")
                return

            from tkinter import ttk
            tk.Label(wrap, text="Categoría destino:").pack(anchor="w")
            cb = ttk.Combobox(wrap, state="readonly", width=44,
                            values=[f"{d[0]} - {d[1]}" for d in destinos])
            cb.pack(fill="x", pady=(4,10))
            cb.current(0)

            def reasignar_y_eliminar():
                val = cb.get().strip()
                if not val:
                    messagebox.showwarning("Atención", "Seleccioná una categoría destino.")
                    return
                id_destino = int(val.split(" - ")[0])

                conn3 = get_connection(); c3 = conn3.cursor()
                try:
                    # Transacción: reasignar y luego eliminar
                    c3.execute("UPDATE assets SET id_categoria = ? WHERE id_categoria = ?", (id_destino, id_categoria))
                    c3.execute("DELETE FROM categorias_asset WHERE id_categoria = ?", (id_categoria,))
                    conn3.commit()
                    messagebox.showinfo("Éxito", f"Activos reasignados y categoría '{nombre}' eliminada.")
                    popup.destroy()
                    self.load_categorias()
                except Exception as e:
                    conn3.rollback()
                    messagebox.showerror("Error", f"No se pudo completar la operación: {e}")
                finally:
                    conn3.close()

            tk.Button(wrap, text="Reasignar y eliminar", command=reasignar_y_eliminar, **BTN_KW).pack(fill="x", pady=(4,0))
            tk.Button(wrap, text="Cancelar", command=popup.destroy).pack(pady=(8,0))
            return

        # Sin assets: eliminación directa
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la categoría '{nombre}'?"):
            conn.close()
            return

        try:
            cur.execute("DELETE FROM categorias_asset WHERE id_categoria = ?", (id_categoria,))
            conn.commit()
            messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
            self.load_categorias()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
        finally:
            conn.close()

