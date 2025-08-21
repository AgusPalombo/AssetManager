import tkinter as tk
from tkinter import messagebox
import bcrypt
from database.connection import get_connection
from ui.main_window import MainWindow
from ui.components.ui_theme import FONT_LABEL, FONT_TITLE, BTN_KW

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login - Asset Management")
        master.geometry("400x300")
        master.resizable(False, False)

        wrap = tk.Frame(master, padx=12, pady=12)
        wrap.pack(fill="both", expand=True)

        title = tk.Label(wrap, text="Iniciar sesión", font=FONT_TITLE)
        title.pack(pady=(0, 10))

        tk.Label(wrap, text="Usuario:", font=FONT_LABEL).pack(anchor="w")
        self.entry_user = tk.Entry(wrap, width=30)
        self.entry_user.pack(pady=(0, 8))

        tk.Label(wrap, text="Contraseña:", font=FONT_LABEL).pack(anchor="w")
        self.entry_pass = tk.Entry(wrap, show="*", width=30)
        self.entry_pass.pack(pady=(0, 12))

        self.button_login = tk.Button(wrap, text="Iniciar Sesión", command=self.login, **BTN_KW)
        self.button_login.pack(pady=(4, 4))

        self.entry_user.focus_set()

    def login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, rol FROM usuarios WHERE nombre = ? AND activo = 1", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            stored_hash, rol = row
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                messagebox.showinfo("Éxito", f"Bienvenido {username} ({rol})")
                self.master.destroy()
                root = tk.Tk()
                MainWindow(root, username, rol)
                root.mainloop()
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
