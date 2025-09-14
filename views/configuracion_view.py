# views/configuracion_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils.config_manager import ConfigManager

class ConfiguracionView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.config_manager = ConfigManager(app.get_db())
        self.setup_ui()
        
    def setup_ui(self):
        # Configuración de IVA
        iva_frame = ttk.LabelFrame(self.frame, text="Configuración de IVA")
        iva_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(iva_frame, text="Porcentaje de IVA (%):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.iva_entry = ttk.Entry(iva_frame, width=10)
        self.iva_entry.insert(0, str(self.app.get_config()['porcentaje_iva']))
        self.iva_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Configuración de descuentos
        descuento_frame = ttk.LabelFrame(self.frame, text="Configuración de Descuentos")
        descuento_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(descuento_frame, text="Descuento por pago en efectivo (%):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.descuento_efectivo_entry = ttk.Entry(descuento_frame, width=10)
        self.descuento_efectivo_entry.insert(0, str(self.app.get_config()['descuento_efectivo']))
        self.descuento_efectivo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.habilitar_descuento_var = tk.BooleanVar(value=self.app.get_config()['habilitar_descuento_efectivo'])
        ttk.Checkbutton(descuento_frame, text="Habilitar descuento por pago en efectivo", 
                       variable=self.habilitar_descuento_var).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        
        self.habilitar_cupones_var = tk.BooleanVar(value=self.app.get_config()['habilitar_cupones'])
        ttk.Checkbutton(descuento_frame, text="Habilitar sistema de cupones", 
                       variable=self.habilitar_cupones_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        
        # Botón guardar configuración
        ttk.Button(self.frame, text="Guardar Configuración", command=self.guardar_configuracion).pack(pady=10)
    
    def guardar_configuracion(self):
        """Guarda la configuración del sistema"""
        try:
            iva = float(self.iva_entry.get())
            descuento_efectivo = float(self.descuento_efectivo_entry.get())
            
            # Actualizar configuración
            nueva_config = {
                'porcentaje_iva': iva,
                'descuento_efectivo': descuento_efectivo,
                'habilitar_descuento_efectivo': self.habilitar_descuento_var.get(),
                'habilitar_cupones': self.habilitar_cupones_var.get()
            }
            
            # Guardar en base de datos
            self.config_manager.guardar_configuracion(nueva_config)
            
            # Actualizar configuración en la aplicación
            self.app.configuracion = nueva_config
            
            # Actualizar etiqueta de IVA en la pestaña de facturación
            if hasattr(self.app, 'facturacion_view'):
                self.app.facturacion_view.iva_label.config(text=f"IVA ({iva}%):")
            
            # Recalcular totales de la factura actual
            if hasattr(self.app, 'facturacion_view'):
                self.app.facturacion_view.calcular_totales()
            
            # Recargar la pestaña de cupones si es necesario
            if hasattr(self.app, 'cupones_view'):
                for widget in self.app.cupones_view.frame.winfo_children():
                    widget.destroy()
                self.app.cupones_view.setup_ui()
                if nueva_config['habilitar_cupones']:
                    self.app.cupones_view.load_cupones()

            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "Los valores de IVA y descuento deben ser números válidos")
    
    def actualizar_vista(self):
        """Actualiza la vista con la configuración actual"""
        self.iva_entry.delete(0, tk.END)
        self.iva_entry.insert(0, str(self.app.get_config()['porcentaje_iva']))
        
        self.descuento_efectivo_entry.delete(0, tk.END)
        self.descuento_efectivo_entry.insert(0, str(self.app.get_config()['descuento_efectivo']))
        
        self.habilitar_descuento_var.set(self.app.get_config()['habilitar_descuento_efectivo'])
        self.habilitar_cupones_var.set(self.app.get_config()['habilitar_cupones'])