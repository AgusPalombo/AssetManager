import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database.users_dao import (
    list_users, get_user_by_name, create_user, update_user,
    reset_password, set_active, delete_user, count_admins
)

ROLES = ("admin", "usuario")

class UsersWindow:
    def __init__(self, master, current_username: str):
        self.master = master
        self.current_username = current_username
        master.title("Gestión de Usuarios")
        master.geometry("820x450")
        master.resizable(False, False)

        self.tree = ttk.Treeview(master, columns=("id","nombre","rol","activo"), show="headings")
        for col, txt, w in [("id","ID",70), ("nombre","Usuario",260), ("rol","Rol",120), ("activo","Activo",80)]:
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=10)

        btns = tk.Frame(master)
        btns.pack(pady=5)

        tk.Button(btns, text="Agregar", width=16, height=2, command=self.add_user).grid(row=0, column=0, padx=6)
        tk.Button(btns, text="Editar", width=16, height=2, command=self.edit_user).grid(row=0, column=1, padx=6)
        tk.Button(btns, text="Reset Password", width=16, height=2, command=self.reset_user_password).grid(row=0, column=2, padx=6)
        tk.Button(btns, text="Activar/Desactivar", width=16, height=2, command=self.toggle_active).grid(row=0, column=3, padx=6)
        tk.Button(btns, text="Eliminar", width=16, height=2, command=self.remove_user).grid(row=0, column=4, padx=6)
        tk.Button(btns, text="Refrescar", width=16, height=2, command=self.load).grid(row=0, column=5, padx=6)

        self.load()

    def load(self):
        for it in self.tree.get_children():
            self.tree.delete(it)
        for uid, nombre, rol, activo in list_users():
            self.tree.insert("", tk.END, values=(uid, nombre, rol, "Sí" if activo else "No"))

    # --- Helpers ---
    def _selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un usuario.")
            return None
        return self.tree.item(sel[0])["values"]  # (id, nombre, rol, activo_text)

    def _is_last_admin_guard(self, target_user_id: int, action: str) -> bool:
        """True si la acción debe bloquearse por dejar sin admins."""
        # Si estamos afectando a un admin activo y es el último, bloquear
        admins = count_admins()
        # Para borrar o desactivar a un admin, no dejar si admins == 1
        if admins <= 1:
            # Consultar si el target es admin activo actualmente
            for uid, nombre, rol, activo in list_users():
                if uid == target_user_id and rol == "admin" and activo == 1:
                    messagebox.showerror("Bloqueado", f"No podés {action} al último administrador activo.")
                    return True
        return False

    # --- Actions ---
    def add_user(self):
        popup = tk.Toplevel(self.master)
        popup.title("Nuevo Usuario")
        popup.geometry("420x250")
        popup.resizable(False, False)

        tk.Label(popup, text="Usuario:").pack(anchor="w", pady=(10, 0))
        e_user = tk.Entry(popup, width=42); e_user.pack()

        tk.Label(popup, text="Rol (admin/usuario):").pack(anchor="w", pady=(8, 0))
        rol_var = tk.StringVar(value="usuario")
        rol_combo = ttk.Combobox(popup, textvariable=rol_var, values=ROLES, width=39, state="readonly")
        rol_combo.pack()

        tk.Label(popup, text="Contraseña:").pack(anchor="w", pady=(8, 0))
        e_pass = tk.Entry(popup, show="*", width=42); e_pass.pack()

        tk.Label(popup, text="Repetir contraseña:").pack(anchor="w", pady=(8, 0))
        e_pass2 = tk.Entry(popup, show="*", width=42); e_pass2.pack()

        def save():
            user = e_user.get().strip()
            rol = rol_var.get()
            p1, p2 = e_pass.get(), e_pass2.get()

            if not user or not p1:
                messagebox.showerror("Error", "Usuario y contraseña son obligatorios.")
                return
            if rol not in ROLES:
                messagebox.showerror("Error", "Rol inválido.")
                return
            if p1 != p2:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return
            try:
                create_user(user, p1, rol)
                messagebox.showinfo("Éxito", "Usuario creado.")
                popup.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear: {e}")

        tk.Button(popup, text="Guardar", width=18, height=2, command=save).pack(pady=12)

    def edit_user(self):
        sel = self._selected()
        if not sel: return
        uid, nombre, rol, activo_text = sel

        popup = tk.Toplevel(self.master)
        popup.title(f"Editar Usuario #{uid}")
        popup.geometry("420x220")
        popup.resizable(False, False)

        tk.Label(popup, text="Usuario:").pack(anchor="w", pady=(10, 0))
        e_user = tk.Entry(popup, width=42); e_user.insert(0, nombre); e_user.pack()

        tk.Label(popup, text="Rol (admin/usuario):").pack(anchor="w", pady=(8, 0))
        rol_var = tk.StringVar(value=rol)
        rol_combo = ttk.Combobox(popup, textvariable=rol_var, values=ROLES, width=39, state="readonly")
        rol_combo.pack()

        def save():
            new_user = e_user.get().strip()
            new_role = rol_var.get()
            if not new_user: 
                messagebox.showerror("Error", "Usuario obligatorio.")
                return
            # Evitar dejar sin admins si se cambia el único admin a 'usuario'
            if rol == "admin" and new_role != "admin" and self._is_last_admin_guard(uid, "editar"):
                return
            try:
                update_user(uid, new_user, new_role)
                messagebox.showinfo("Éxito", "Usuario actualizado.")
                popup.destroy()
                self.load()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        tk.Button(popup, text="Guardar cambios", width=18, height=2, command=save).pack(pady=12)

    def reset_user_password(self):
        sel = self._selected()
        if not sel: return
        uid, nombre, rol, activo_text = sel

        new_pass = simpledialog.askstring("Reset Password", f"Nueva contraseña para '{nombre}':", show="*")
        if not new_pass: return
        if len(new_pass) < 6:
            messagebox.showwarning("Atención", "La contraseña debe tener al menos 6 caracteres.")
            return
        try:
            reset_password(uid, new_pass)
            messagebox.showinfo("Éxito", "Contraseña actualizada.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")

    def toggle_active(self):
        sel = self._selected()
        if not sel: return
        uid, nombre, rol, activo_text = sel
        new_state = 0 if activo_text == "Sí" else 1

        # No permitir desactivar al último admin activo
        if new_state == 0 and self._is_last_admin_guard(uid, "desactivar"):
            return

        # Evitar que el usuario actual se auto-desactive accidentalmente
        if nombre == self.current_username and new_state == 0:
            messagebox.showerror("Bloqueado", "No podés desactivar tu propio usuario en sesión.")
            return

        try:
            set_active(uid, bool(new_state))
            messagebox.showinfo("Éxito", f"Usuario {'activado' if new_state==1 else 'desactivado'}.")
            self.load()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cambiar el estado: {e}")

    def remove_user(self):
        sel = self._selected()
        if not sel: return
        uid, nombre, rol, activo_text = sel

        if nombre == self.current_username:
            messagebox.showerror("Bloqueado", "No podés eliminar el usuario con el que estás logueado.")
            return
        if self._is_last_admin_guard(uid, "eliminar"):
            return

        if not messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{nombre}'?"):
            return
        try:
            delete_user(uid)
            messagebox.showinfo("Éxito", "Usuario eliminado.")
            self.load()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")