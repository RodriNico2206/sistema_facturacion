# dialogs/cliente_manual_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import Cliente

class ClienteManualDialog:
    def __init__(self, parent, app, combobox_widget):
        self.app = app
        self.combobox_widget = combobox_widget
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Datos del Cliente")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Centrar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Campos del formulario
        ttk.Label(self.dialog, text="Nombre:*").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.nombre_entry = ttk.Entry(self.dialog, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=10)
        self.nombre_entry.focus()
        
        ttk.Label(self.dialog, text="DNI:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.dni_entry = ttk.Entry(self.dialog, width=30)
        self.dni_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(self.dialog, text="Dirección:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.direccion_entry = ttk.Entry(self.dialog, width=30)
        self.direccion_entry.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(self.dialog, text="Teléfono:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.telefono_entry = ttk.Entry(self.dialog, width=30)
        self.telefono_entry.grid(row=3, column=1, padx=10, pady=10)
        
        ttk.Label(self.dialog, text="Email:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.email_entry = ttk.Entry(self.dialog, width=30)
        self.email_entry.grid(row=4, column=1, padx=10, pady=10)
        
        # Botones
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Usar Cliente", command=self.guardar_cliente_manual).pack(side='right', padx=10)
    
    def guardar_cliente_manual(self):
        nombre = self.nombre_entry.get().strip()
        dni = self.dni_entry.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        # Crear objeto cliente manual
        self.app.cliente_manual = Cliente(
            nombre=nombre,
            dni=dni,
            direccion=self.direccion_entry.get().strip(),
            telefono=self.telefono_entry.get().strip(),
            email=self.email_entry.get().strip()
        )
        
        # Actualizar combobox para mostrar el cliente manual
        self.combobox_widget.set(f"{nombre} (DNI: {dni}) - MANUAL")
        self.dialog.destroy()