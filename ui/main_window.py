import tkinter as tk
from ui.components.categorias import CategoriasWindow
from ui.components.activos import ActivosWindow
from ui.components.users import UsersWindow
from ui.components.ui_theme import FONT_TITLE, BTN_KW

class MainWindow:
    def __init__(self, master, username, rol):
        self.master = master
        self.username = username
        self.rol = rol

        master.title("Asset Management - Principal")
        master.geometry("460x380")

        wrap = tk.Frame(master, padx=12, pady=12)
        wrap.pack(fill="both", expand=True)

        title = tk.Label(wrap, text=f"Bienvenido {username}  ·  Rol: {rol}", font=FONT_TITLE)
        title.pack(pady=(0, 12))

        # --- Siempre visible ---
        self.btn_assets = tk.Button(
            wrap, text="Gestionar Activos",
            command=self.open_activos, **BTN_KW
        )
        self.btn_assets.pack(pady=5, fill="x")

        # --- Solo admin: Categorías y Usuarios ---
        if rol == "admin":
            self.btn_categorias = tk.Button(
                wrap, text="Gestionar Categorías",
                command=self.open_categorias, **BTN_KW
            )
            self.btn_categorias.pack(pady=5, fill="x")

            self.btn_usuarios = tk.Button(
                wrap, text="Gestionar Usuarios",
                command=self.open_usuarios, **BTN_KW
            )
            self.btn_usuarios.pack(pady=5, fill="x")

        self.btn_salir = tk.Button(
            wrap, text="Salir", command=master.quit, **BTN_KW
        )
        self.btn_salir.pack(pady=14, fill="x")

    # --- Handlers ---
    def open_activos(self):
        new_win = tk.Toplevel(self.master)
        ActivosWindow(new_win, current_username=self.username, current_role=self.rol)

    def open_categorias(self):
        # Defensa extra: bloquear apertura si no es admin
        if self.rol != "admin":
            from tkinter import messagebox
            messagebox.showerror("Permisos", "No tenés permisos para gestionar categorías.")
            return
        new_win = tk.Toplevel(self.master)
        CategoriasWindow(new_win, current_username=self.username, current_role=self.rol)

    def open_usuarios(self):
        # Defensa extra: bloquear apertura si no es admin
        if self.rol != "admin":
            from tkinter import messagebox
            messagebox.showerror("Permisos", "No tenés permisos para gestionar usuarios.")
            return
        new_win = tk.Toplevel(self.master)
        UsersWindow(new_win, current_username=self.username)