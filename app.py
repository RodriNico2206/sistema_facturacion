# # app.py
# from tkinter import ttk
# from database import Database
# from invoice_generator import InvoiceGenerator
# from views.facturacion_view import FacturacionView
# from views.clientes_view import ClientesView
# from views.productos_view import ProductosView
# from views.configuracion_view import ConfiguracionView
# from views.cupones_view import CuponesView
# from utils.config_manager import ConfigManager

# class FacturacionApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Sistema de Facturación")
#         self.root.geometry("1200x700")
        
#         self.db = Database()
#         self.invoice_gen = InvoiceGenerator()
#         self.config_manager = ConfigManager(self.db)
        
#         self.current_factura = None
#         self.detalles_temp = []
#         self.configuracion = self.config_manager.cargar_configuracion()
#         self.cupon_aplicado = None
        
#         self.setup_ui()
#         self.load_data()

#     def setup_ui(self):
#         self.notebook = ttk.Notebook(self.root)
#         self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
#         # Crear las vistas para cada pestaña
#         self.facturacion_view = FacturacionView(self.notebook, self)
#         self.clientes_view = ClientesView(self.notebook, self)
#         self.productos_view = ProductosView(self.notebook, self)
#         self.configuracion_view = ConfiguracionView(self.notebook, self)
#         self.cupones_view = CuponesView(self.notebook, self)
        
#         # Añadir las pestañas
#         self.notebook.add(self.facturacion_view.frame, text="Facturación")
#         self.notebook.add(self.clientes_view.frame, text="Clientes")
#         self.notebook.add(self.productos_view.frame, text="Productos")
#         self.notebook.add(self.configuracion_view.frame, text="Configuración")
#         self.notebook.add(self.cupones_view.frame, text="Cupones")

#     def load_data(self):
#         self.clientes_view.load_clientes()
#         self.productos_view.load_productos()
#         if self.configuracion['habilitar_cupones']:
#             self.cupones_view.load_cupones()

#     # Métodos de utilidad que pueden ser accedidos desde las vistas
#     def get_db(self):
#         return self.db
        
#     def get_config(self):
#         return self.configuracion
        
#     def update_config(self, nueva_config):
#         self.configuracion = nueva_config
#         self.configuracion_view.actualizar_vista()
#         if hasattr(self, 'cupones_view'):
#             self.cupones_view.actualizar_vista()
            
#     def get_invoice_gen(self):
#         return self.invoice_gen


# app.py (modificación)
from tkinter import ttk
from database import Database
from utils.invoice_generator import InvoiceGenerator
from views.facturacion_view import FacturacionView
from views.clientes_view import ClientesView
from views.productos_view import ProductosView
from views.configuracion_view import ConfiguracionView
from views.cupones_view import CuponesView
from views.facturas_view import FacturasView  # <-- Añadir esta importación
from utils.config_manager import ConfigManager

class FacturacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Facturación")
        self.root.geometry("1200x700")
        
        self.db = Database()
        self.invoice_gen = InvoiceGenerator()
        self.config_manager = ConfigManager(self.db)
        
        self.current_factura = None
        self.detalles_temp = []
        self.configuracion = self.config_manager.cargar_configuracion()
        self.cupon_aplicado = None
        
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear las vistas para cada pestaña
        self.facturacion_view = FacturacionView(self.notebook, self)
        self.clientes_view = ClientesView(self.notebook, self)
        self.productos_view = ProductosView(self.notebook, self)
        self.configuracion_view = ConfiguracionView(self.notebook, self)
        self.cupones_view = CuponesView(self.notebook, self)
        self.facturas_view = FacturasView(self.notebook, self)  # <-- Añadir esta línea
        
        # Añadir las pestañas
        self.notebook.add(self.facturacion_view.frame, text="Facturación")
        self.notebook.add(self.clientes_view.frame, text="Clientes")
        self.notebook.add(self.productos_view.frame, text="Productos")
        self.notebook.add(self.configuracion_view.frame, text="Configuración")
        self.notebook.add(self.cupones_view.frame, text="Cupones")
        self.notebook.add(self.facturas_view.frame, text="Facturas")  # <-- Añadir esta línea

    def load_data(self):
        self.clientes_view.load_clientes()
        self.productos_view.load_productos()
        if self.configuracion['habilitar_cupones']:
            self.cupones_view.load_cupones()
        self.facturas_view.load_facturas()  # <-- Añadir esta línea

    # Métodos de utilidad que pueden ser accedidos desde las vistas
    def get_db(self):
        return self.db
        
    def get_config(self):
        return self.configuracion
        
    def update_config(self, nueva_config):
        self.configuracion = nueva_config
        self.configuracion_view.actualizar_vista()
        if hasattr(self, 'cupones_view'):
            self.cupones_view.actualizar_vista()
            
    def get_invoice_gen(self):
        return self.invoice_gen
    
    def after(self, ms, func):
        """Wrapper para el método after de Tkinter"""
        return self.root.after(ms, func)