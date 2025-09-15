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
    
    # def mostrar_dialogo_usuario(self, usuario_data=None):
    #     dialog = tk.Toplevel(self.frame)
    #     dialog.title("Agregar Usuario" if not usuario_data else "Editar Usuario")
    #     dialog.geometry("400x300")
    #     dialog.resizable(False, False)
        
    #     # Campos del formulario...
    #     # (Implementar formulario similar al de clientes/productos)

    def mostrar_dialogo_usuario(self, usuario_data=None):
        dialog = tk.Toplevel(self.frame)
        dialog.title("Agregar Usuario" if not usuario_data else "Editar Usuario")
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Variables para los campos
        username_var = tk.StringVar()
        nombre_var = tk.StringVar()
        email_var = tk.StringVar()
        activo_var = tk.BooleanVar(value=True)
        
        # Llenar campos si es edición
        if usuario_data:
            username_var.set(usuario_data[1])
            nombre_var.set(usuario_data[2])
            email_var.set(usuario_data[3] if usuario_data[3] else "")
            activo_var.set(bool(usuario_data[4]))
        
        # Marco principal
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Campos del formulario
        ttk.Label(main_frame, text="Usuario:*").grid(row=0, column=0, sticky='w', pady=5)
        username_entry = ttk.Entry(main_frame, textvariable=username_var, width=30)
        username_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(main_frame, text="Nombre:*").grid(row=1, column=0, sticky='w', pady=5)
        nombre_entry = ttk.Entry(main_frame, textvariable=nombre_var, width=30)
        nombre_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        email_entry = ttk.Entry(main_frame, textvariable=email_var, width=30)
        email_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Checkbutton(main_frame, text="Usuario activo", variable=activo_var).grid(row=3, column=1, sticky='w', pady=10)
        
        # Solo mostrar campo de contraseña para nuevos usuarios
        if not usuario_data:
            ttk.Label(main_frame, text="Contraseña:*").grid(row=4, column=0, sticky='w', pady=5)
            password_var = tk.StringVar()
            password_entry = ttk.Entry(main_frame, textvariable=password_var, show='•', width=30)
            password_entry.grid(row=4, column=1, padx=5, pady=5, sticky='ew')
        else:
            password_var = None
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def guardar_usuario():
            username = username_var.get().strip()
            nombre = nombre_var.get().strip()
            email = email_var.get().strip()
            activo = activo_var.get()
            
            if not username or not nombre:
                messagebox.showerror("Error", "Usuario y nombre son obligatorios")
                return
            
            if not usuario_data and (not password_var or not password_var.get().strip()):
                messagebox.showerror("Error", "La contraseña es obligatoria para nuevos usuarios")
                return
            
            try:
                db = self.app.get_db()
                
                if usuario_data:  # Edición
                    if email:
                        db.execute_query(
                            "UPDATE usuarios SET username=?, nombre=?, email=?, activo=? WHERE id=?",
                            (username, nombre, email, 1 if activo else 0, usuario_data[0])
                        )
                    else:
                        db.execute_query(
                            "UPDATE usuarios SET username=?, nombre=?, activo=? WHERE id=?",
                            (username, nombre, 1 if activo else 0, usuario_data[0])
                        )
                else:  # Nuevo usuario
                    password = password_var.get().strip()
                    password_hash = db.hash_password(password)
                    
                    if email:
                        db.execute_query(
                            "INSERT INTO usuarios (username, password, nombre, email, activo) VALUES (?, ?, ?, ?, ?)",
                            (username, password_hash, nombre, email, 1 if activo else 0)
                        )
                    else:
                        db.execute_query(
                            "INSERT INTO usuarios (username, password, nombre, activo) VALUES (?, ?, ?, ?)",
                            (username, password_hash, nombre, 1 if activo else 0)
                        )
                
                self.load_usuarios()
                dialog.destroy()
                messagebox.showinfo("Éxito", "Usuario guardado correctamente")
                
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    messagebox.showerror("Error", "El nombre de usuario ya existe")
                else:
                    messagebox.showerror("Error", f"Error al guardar usuario: {str(e)}")
        
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Guardar", command=guardar_usuario).pack(side='right', padx=10)
        
        # Enfocar el primer campo
        username_entry.focus()

    # def mostrar_dialogo_password(self, usuario_id):
    #     dialog = tk.Toplevel(self.frame)
    #     dialog.title("Cambiar Contraseña")
    #     dialog.geometry("300x200")
    #     dialog.resizable(False, False)


    def mostrar_dialogo_password(self, usuario_id):
        dialog = tk.Toplevel(self.frame)
        dialog.title("Cambiar Contraseña")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Obtener información del usuario
        db = self.app.get_db()
        usuario = db.fetch_one("SELECT username, nombre FROM usuarios WHERE id = ?", (usuario_id,))
        
        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado")
            dialog.destroy()
            return
        
        # Variables para los campos
        nueva_password_var = tk.StringVar()
        confirmar_password_var = tk.StringVar()
        
        # Marco principal
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Información del usuario
        ttk.Label(main_frame, text=f"Usuario: {usuario[0]}", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 10))
        ttk.Label(main_frame, text=f"Nombre: {usuario[1]}", font=('Arial', 10)).pack(anchor='w', pady=(0, 20))
        
        # Campos de contraseña
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill='x', pady=10)
        
        ttk.Label(form_frame, text="Nueva contraseña:*").grid(row=0, column=0, sticky='w', pady=5)
        nueva_password_entry = ttk.Entry(form_frame, textvariable=nueva_password_var, show='•', width=25)
        nueva_password_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        ttk.Label(form_frame, text="Confirmar contraseña:*").grid(row=1, column=0, sticky='w', pady=5)
        confirmar_password_entry = ttk.Entry(form_frame, textvariable=confirmar_password_var, show='•', width=25)
        confirmar_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        def cambiar_password():
            nueva_password = nueva_password_var.get().strip()
            confirmar_password = confirmar_password_var.get().strip()
            
            if not nueva_password:
                messagebox.showerror("Error", "La nueva contraseña es obligatoria")
                return
            
            if nueva_password != confirmar_password:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            
            if len(nueva_password) < 6:
                messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
                return
            
            try:
                password_hash = db.hash_password(nueva_password)
                db.execute_query(
                    "UPDATE usuarios SET password = ? WHERE id = ?",
                    (password_hash, usuario_id)
                )
                
                dialog.destroy()
                messagebox.showinfo("Éxito", "Contraseña cambiada correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cambiar contraseña: {str(e)}")
        
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cambiar Contraseña", command=cambiar_password).pack(side='right', padx=10)
        
        # Enfocar el primer campo y bindear Enter
        nueva_password_entry.focus()
        nueva_password_entry.bind('<Return>', lambda e: cambiar_password())
        confirmar_password_entry.bind('<Return>', lambda e: cambiar_password())

        
        # Campos para cambiar contraseña...