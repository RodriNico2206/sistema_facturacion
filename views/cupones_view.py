# views/cupones_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from dialogs.cupon_dialog import CuponDialog

class CuponesView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        
    def setup_ui(self):
        if not self.app.get_config()['habilitar_cupones']:
            ttk.Label(self.frame, text="Los cupones están deshabilitados en la configuración").pack(pady=20)
            return
        
        # Treeview para cupones
        columns = ('id', 'codigo', 'descuento', 'valido_desde', 'valido_hasta', 'usos_maximos', 'usos_actuales', 'activo')
        self.cupones_tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.cupones_tree.heading(col, text=col.capitalize())
            self.cupones_tree.column(col, width=100)
        
        self.cupones_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botones para cupones
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Agregar Cupón", command=self.agregar_cupon).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Editar Cupón", command=self.editar_cupon).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Eliminar Cupón", command=self.eliminar_cupon).pack(side='left', padx=5)
        
        self.load_cupones()
    
    def load_cupones(self):
        """Carga los cupones desde la base de datos"""
        if not self.app.get_config()['habilitar_cupones']:
            return
            
        cupones = self.app.get_db().fetch_all("SELECT * FROM cupones ORDER BY codigo")
        
        for item in self.cupones_tree.get_children():
            self.cupones_tree.delete(item)
        
        for cupon in cupones:
            self.cupones_tree.insert('', 'end', values=cupon)
    
    def agregar_cupon(self):
        CuponDialog(self.frame, self.app, self.load_cupones)
    
    def editar_cupon(self):
        selection = self.cupones_tree.selection()
        if selection:
            item = self.cupones_tree.item(selection[0])
            CuponDialog(self.frame, self.app, self.load_cupones, item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un cupón para editar")
    
    def eliminar_cupon(self):
        selection = self.cupones_tree.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cupón?"):
                item = self.cupones_tree.item(selection[0])
                try:
                    self.app.get_db().execute_query("DELETE FROM cupones WHERE id = ?", (item['values'][0],))
                    self.load_cupones()
                    messagebox.showinfo("Éxito", "Cupón eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar cupón: {str(e)}")
        else:
            messagebox.showerror("Error", "Seleccione un cupón para eliminar")
    
    def actualizar_vista(self):
        """Actualiza la vista cuando cambia la configuración"""
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.setup_ui()