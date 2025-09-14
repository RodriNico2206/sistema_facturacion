# dialogs/cliente_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox

class ClienteDialog:
    def __init__(self, parent, app, callback, cliente_data=None):
        self.app = app
        self.callback = callback
        self.cliente_data = cliente_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Cliente" if not cliente_data else "Editar Cliente")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Centrar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Campos del formulario
        ttk.Label(self.dialog, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.nombre_entry = ttk.Entry(self.dialog, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="DNI:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.dni_entry = ttk.Entry(self.dialog, width=30)
        self.dni_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Dirección:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.direccion_entry = ttk.Entry(self.dialog, width=30)
        self.direccion_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.telefono_entry = ttk.Entry(self.dialog, width=30)
        self.telefono_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Email:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.email_entry = ttk.Entry(self.dialog, width=30)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Llenar campos si es edición
        if self.cliente_data:
            self.nombre_entry.insert(0, self.cliente_data[1])
            self.dni_entry.insert(0, self.cliente_data[2])
            self.direccion_entry.insert(0, self.cliente_data[3])
            self.telefono_entry.insert(0, self.cliente_data[4])
            self.email_entry.insert(0, self.cliente_data[5])
        
        # Botones
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_cliente).pack(side='right', padx=10)
        
        self.nombre_entry.focus()
    
    def guardar_cliente(self):
        nombre = self.nombre_entry.get().strip()
        dni = self.dni_entry.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        try:
            if self.cliente_data:  # Edición
                self.app.get_db().execute_query(
                    "UPDATE clientes SET nombre=?, dni=?, direccion=?, telefono=?, email=? WHERE id=?",
                    (nombre, dni, self.direccion_entry.get(), self.telefono_entry.get(), 
                     self.email_entry.get(), self.cliente_data[0])
                )
            else:  # Inserción
                self.app.get_db().execute_query(
                    "INSERT INTO clientes (nombre, dni, direccion, telefono, email) VALUES (?, ?, ?, ?, ?)",
                    (nombre, dni, self.direccion_entry.get(), self.telefono_entry.get(), self.email_entry.get())
                )
            
            self.callback()
            self.dialog.destroy()
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cliente: {str(e)}")