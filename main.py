from database.create_db import create_tables
from database.create_admin import create_admin_user
import tkinter as tk
from ui.components.login import LoginWindow

if __name__ == "__main__":
    create_tables()
    create_admin_user()

    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
