from database.create_db import create_tables
from database.default_categories import seed_default_categories
from database.create_admin import create_admin_user
import tkinter as tk
from ui.components.login import LoginWindow

if __name__ == "__main__":
    create_tables()
    seed_default_categories()
    create_admin_user()

    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
