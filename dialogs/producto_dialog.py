# dialogs/producto_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox

class ProductoDialog:
    def __init__(self, parent, app, callback, producto_data=None):
        self.app = app
        self.callback = callback
        self.producto_data = producto_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Producto" if not producto_data else "Editar Producto")
        self.dialog.geometry("400x350")
        self.dialog.resizable(False, False)
        
        # Centrar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Campos del formulario
        ttk.Label(self.dialog, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.codigo_entry = ttk.Entry(self.dialog, width=30)
        self.codigo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.nombre_entry = ttk.Entry(self.dialog, width=30)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Descripción:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.descripcion_entry = ttk.Entry(self.dialog, width=30)
        self.descripcion_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Precio:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.precio_entry = ttk.Entry(self.dialog, width=30)
        self.precio_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Stock:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.stock_entry = ttk.Entry(self.dialog, width=30)
        self.stock_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Llenar campos si es edición
        if self.producto_data:
            self.codigo_entry.insert(0, self.producto_data[1])
            self.nombre_entry.insert(0, self.producto_data[2])
            self.descripcion_entry.insert(0, self.producto_data[3])
            self.precio_entry.insert(0, str(self.producto_data[4]))
            self.stock_entry.insert(0, str(self.producto_data[5]))
        
        # Botones
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_producto).pack(side='right', padx=10)
        
        self.codigo_entry.focus()
    
    def guardar_producto(self):
        codigo = self.codigo_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        precio = self.precio_entry.get().strip()
        stock = self.stock_entry.get().strip()
        
        if not all([codigo, nombre, precio]):
            messagebox.showerror("Error", "Código, nombre y precio son obligatorios")
            return
        
        try:
            precio_val = float(precio)
            stock_val = int(stock) if stock else 0
            
            if self.producto_data:  # Edición
                self.app.get_db().execute_query(
                    "UPDATE productos SET codigo=?, nombre=?, descripcion=?, precio=?, stock=? WHERE id=?",
                    (codigo, nombre, self.descripcion_entry.get(), precio_val, stock_val, self.producto_data[0])
                )
            else:  # Inserción
                self.app.get_db().execute_query(
                    "INSERT INTO productos (codigo, nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?, ?)",
                    (codigo, nombre, self.descripcion_entry.get(), precio_val, stock_val)
                )
            
            self.callback()
            self.dialog.destroy()
            messagebox.showinfo("Éxito", "Producto guardado correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "Precio y stock deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar producto: {str(e)}")