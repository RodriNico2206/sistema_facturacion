# main.py
import tkinter as tk
from app import FacturacionApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FacturacionApp(root)
    root.mainloop()