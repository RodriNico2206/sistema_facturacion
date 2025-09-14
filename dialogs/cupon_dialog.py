# dialogs/cupon_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox

class CuponDialog:
    def __init__(self, parent, app, callback, cupon_data=None):
        self.app = app
        self.callback = callback
        self.cupon_data = cupon_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Cupón" if not cupon_data else "Editar Cupón")
        self.dialog.geometry("400x400")
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
        
        ttk.Label(self.dialog, text="Descuento (%):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.descuento_entry = ttk.Entry(self.dialog, width=30)
        self.descuento_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.dialog, text="Válido desde:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.valido_desde_entry = ttk.Entry(self.dialog, width=30)
        self.valido_desde_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.dialog, text="Formato: YYYY-MM-DD").grid(row=3, column=1, padx=5, sticky='w')
        
        ttk.Label(self.dialog, text="Válido hasta:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.valido_hasta_entry = ttk.Entry(self.dialog, width=30)
        self.valido_hasta_entry.grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(self.dialog, text="Formato: YYYY-MM-DD").grid(row=5, column=1, padx=5, sticky='w')
        
        ttk.Label(self.dialog, text="Usos máximos:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        self.usos_maximos_entry = ttk.Entry(self.dialog, width=30)
        self.usos_maximos_entry.grid(row=6, column=1, padx=5, pady=5)
        
        self.activo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dialog, text="Activo", variable=self.activo_var).grid(row=7, column=1, padx=5, pady=5, sticky='w')
        
        # Llenar campos si es edición
        if self.cupon_data:
            self.codigo_entry.insert(0, self.cupon_data[1])
            self.descuento_entry.insert(0, str(self.cupon_data[2]))
            self.valido_desde_entry.insert(0, self.cupon_data[3] or "")
            self.valido_hasta_entry.insert(0, self.cupon_data[4] or "")
            self.usos_maximos_entry.insert(0, str(self.cupon_data[5]))
            self.activo_var.set(bool(self.cupon_data[7]))
        
        # Botones
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancelar", command=self.dialog.destroy).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Guardar", command=self.guardar_cupon).pack(side='right', padx=10)
        
        self.codigo_entry.focus()
    
    def guardar_cupon(self):
        codigo = self.codigo_entry.get().strip()
        descuento = self.descuento_entry.get().strip()
        
        if not all([codigo, descuento]):
            messagebox.showerror("Error", "Código y descuento son obligatorios")
            return
        
        try:
            descuento_val = float(descuento)
            usos_maximos_val = int(self.usos_maximos_entry.get()) if self.usos_maximos_entry.get() else 1
            
            if self.cupon_data:  # Edición
                self.app.get_db().execute_query(
                    "UPDATE cupones SET codigo=?, descuento=?, valido_desde=?, valido_hasta=?, usos_maximos=?, activo=? WHERE id=?",
                    (codigo, descuento_val, self.valido_desde_entry.get() or None, self.valido_hasta_entry.get() or None, 
                     usos_maximos_val, int(self.activo_var.get()), self.cupon_data[0])
                )
            else:  # Inserción
                self.app.get_db().execute_query(
                    "INSERT INTO cupones (codigo, descuento, valido_desde, valido_hasta, usos_maximos, activo) VALUES (?, ?, ?, ?, ?, ?)",
                    (codigo, descuento_val, self.valido_desde_entry.get() or None, self.valido_hasta_entry.get() or None, 
                     usos_maximos_val, int(self.activo_var.get()))
                )
            
            self.callback()
            self.dialog.destroy()
            messagebox.showinfo("Éxito", "Cupón guardado correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "Descuento y usos máximos deben ser números válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cupón: {str(e)}")