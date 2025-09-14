# views/productos_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from dialogs.producto_dialog import ProductoDialog
from utils.excel_utils import ExcelUtils

class ProductosView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Treeview para productos
        columns = ('id', 'codigo', 'nombre', 'descripcion', 'precio', 'stock')
        self.productos_tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        
        for col in columns:
            self.productos_tree.heading(col, text=col.capitalize())
            self.productos_tree.column(col, width=100)
        
        self.productos_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botones para productos
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)
        
        # Botones a la izquierda
        left_button_frame = ttk.Frame(button_frame)
        left_button_frame.pack(side='left')
        
        ttk.Button(left_button_frame, text="Agregar Producto", command=self.agregar_producto).pack(side='left', padx=5)
        ttk.Button(left_button_frame, text="Editar Producto", command=self.editar_producto).pack(side='left', padx=5)
        ttk.Button(left_button_frame, text="Eliminar Producto", command=self.eliminar_producto).pack(side='left', padx=5)
        
        # Botones a la derecha (Importación/Exportación)
        right_button_frame = ttk.Frame(button_frame)
        right_button_frame.pack(side='right')
        
        ttk.Button(right_button_frame, text="Importar desde Excel", 
                command=self.importar_productos_excel).pack(side='right', padx=5)
        ttk.Button(right_button_frame, text="Exportar a Excel", 
                command=self.exportar_productos_excel).pack(side='right', padx=5)
    
    def load_productos(self):
        # Cargar productos desde la base de datos
        productos = self.app.get_db().fetch_all("SELECT * FROM productos ORDER BY nombre")
        
        # Limpiar treeview
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        # Insertar productos
        for producto in productos:
            self.productos_tree.insert('', 'end', values=producto)
            
        # Actualizar treeview de facturación
        if hasattr(self.app, 'facturacion_view'):
            for item in self.app.facturacion_view.productos_tree.get_children():
                self.app.facturacion_view.productos_tree.delete(item)
            
            for producto in productos:
                # Asegurar que el stock sea un entero
                stock = producto[5]
                try:
                    stock_int = int(float(stock))
                except (ValueError, TypeError):
                    stock_int = 0
                
                # Insertar en el treeview con valores convertidos
                self.app.facturacion_view.productos_tree.insert('', 'end', values=(
                    producto[1],  # codigo
                    producto[2],  # nombre
                    f"${float(producto[4]):.2f}",  # precio
                    stock_int     # stock
                ))
    
    def agregar_producto(self):
        ProductoDialog(self.frame, self.app, self.load_productos)
    
    def editar_producto(self):
        selection = self.productos_tree.selection()
        if selection:
            item = self.productos_tree.item(selection[0])
            ProductoDialog(self.frame, self.app, self.load_productos, item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un producto para editar")
    
    def eliminar_producto(self):
        selection = self.productos_tree.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
                item = self.productos_tree.item(selection[0])
                try:
                    self.app.get_db().execute_query("DELETE FROM productos WHERE id = ?", (item['values'][0],))
                    self.load_productos()
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
        else:
            messagebox.showerror("Error", "Seleccione un producto para eliminar")
    
    def exportar_productos_excel(self):
        ExcelUtils.exportar_productos_excel(self.app.get_db())
    
    def importar_productos_excel(self):
        ExcelUtils.importar_productos_excel(self.app.get_db(), self.load_productos)