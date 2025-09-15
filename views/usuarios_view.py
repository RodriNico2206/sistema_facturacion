# views/usuarios_view.py
import tkinter as tk
from tkinter import ttk, messagebox

class UsuariosView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Treeview para usuarios
        columns = ('id', 'username', 'nombre', 'email', 'activo')
        self.usuarios_tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        
        for col in columns:
            self.usuarios_tree.heading(col, text=col.capitalize())
            self.usuarios_tree.column(col, width=100)
        
        self.usuarios_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botones para usuarios
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Agregar Usuario", command=self.agregar_usuario).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Editar Usuario", command=self.editar_usuario).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cambiar Contraseña", command=self.cambiar_password).pack(side='left', padx=5)
        
        self.load_usuarios()
    
    def load_usuarios(self):
        """Carga los usuarios desde la base de datos"""
        usuarios = self.app.get_db().fetch_all("SELECT id, username, nombre, email, activo FROM usuarios ORDER BY username")
        
        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)
        
        for usuario in usuarios:
            estado = "Activo" if usuario[4] else "Inactivo"
            self.usuarios_tree.insert('', 'end', values=(
                usuario[0], usuario[1], usuario[2], usuario[3], estado
            ))
    
    def agregar_usuario(self):
        self.mostrar_dialogo_usuario()
    
    def editar_usuario(self):
        selection = self.usuarios_tree.selection()
        if selection:
            item = self.usuarios_tree.item(selection[0])
            self.mostrar_dialogo_usuario(item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un usuario para editar")
    
    def cambiar_password(self):
        selection = self.usuarios_tree.selection()
        if selection:
            item = self.usuarios_tree.item(selection[0])
            self.mostrar_dialogo_password(item['values'][0])
        else:
            messagebox.showerror("Error", "Seleccione un usuario para cambiar contraseña")
    
    def mostrar_dialogo_usuario(self, usuario_data=None):
        dialog = tk.Toplevel(self.frame)
        dialog.title("Agregar Usuario" if not usuario_data else "Editar Usuario")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Campos del formulario...
        # (Implementar formulario similar al de clientes/productos)
    
    def mostrar_dialogo_password(self, usuario_id):
        dialog = tk.Toplevel(self.frame)
        dialog.title("Cambiar Contraseña")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        
        # Campos para cambiar contraseña...