# views/clientes_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from dialogs.cliente_dialog import ClienteDialog
from utils.excel_utils import ExcelUtils

class ClientesView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Treeview para clientes
        columns = ('id', 'nombre', 'dni', 'direccion', 'telefono', 'email')
        self.clientes_tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        
        for col in columns:
            self.clientes_tree.heading(col, text=col.capitalize())
            self.clientes_tree.column(col, width=100)
        
        self.clientes_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botones para clientes
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)
        
        # Botones a la izquierda
        left_button_frame = ttk.Frame(button_frame)
        left_button_frame.pack(side='left')
        
        ttk.Button(left_button_frame, text="Agregar Cliente", command=self.agregar_cliente).pack(side='left', padx=5)
        ttk.Button(left_button_frame, text="Editar Cliente", command=self.editar_cliente).pack(side='left', padx=5)
        ttk.Button(left_button_frame, text="Eliminar Cliente", command=self.eliminar_cliente).pack(side='left', padx=5)
        
        # Botones a la derecha (Importación/Exportación)
        right_button_frame = ttk.Frame(button_frame)
        right_button_frame.pack(side='right')
        
        ttk.Button(right_button_frame, text="Importar desde Excel", 
                command=self.importar_clientes_excel).pack(side='right', padx=5)
        ttk.Button(right_button_frame, text="Exportar a Excel", 
                command=self.exportar_clientes_excel).pack(side='right', padx=5)
    
    def load_clientes(self):
        # Cargar clientes en el treeview
        clientes = self.app.get_db().fetch_all("SELECT id, nombre, dni, direccion, telefono, email FROM clientes ORDER BY nombre")
        
        # Limpiar treeview
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        # Insertar clientes
        for cliente in clientes:
            self.clientes_tree.insert('', 'end', values=cliente)
            
        # Actualizar combobox en facturación
        if hasattr(self.app, 'facturacion_view'):
            self.app.facturacion_view.cliente_combobox['values'] = [f"{c[1]} (DNI: {c[2]})" for c in clientes]
    
    def agregar_cliente(self):
        ClienteDialog(self.frame, self.app, self.load_clientes)
    
    def editar_cliente(self):
        selection = self.clientes_tree.selection()
        if selection:
            item = self.clientes_tree.item(selection[0])
            ClienteDialog(self.frame, self.app, self.load_clientes, item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un cliente para editar")
    
    def eliminar_cliente(self):
        selection = self.clientes_tree.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
                item = self.clientes_tree.item(selection[0])
                try:
                    self.app.get_db().execute_query("DELETE FROM clientes WHERE id = ?", (item['values'][0],))
                    self.load_clientes()
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
        else:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
    
    def exportar_clientes_excel(self):
        ExcelUtils.exportar_clientes_excel(self.app.get_db())
    
    def importar_clientes_excel(self):
        ExcelUtils.importar_clientes_excel(self.app.get_db(), self.load_clientes)