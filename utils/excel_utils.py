# utils/excel_utils.py
import pandas as pd
from tkinter import filedialog, messagebox

class ExcelUtils:
    @staticmethod
    def exportar_clientes_excel(db):
        try:
            file_path = filedialog.asksaveasfilename(
                title="Guardar clientes como Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            clientes = db.fetch_all("SELECT nombre, dni, direccion, telefono, email FROM clientes ORDER BY nombre")
            df = pd.DataFrame(clientes, columns=['nombre', 'dni', 'direccion', 'telefono', 'email'])
            df.to_excel(file_path, index=False)
            
            messagebox.showinfo("Éxito", f"Clientes exportados correctamente a: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar clientes: {str(e)}")
    
    @staticmethod
    def exportar_productos_excel(db):
        try:
            file_path = filedialog.asksaveasfilename(
                title="Guardar productos como Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            productos = db.fetch_all("SELECT codigo, nombre, descripcion, precio, stock FROM productos ORDER BY nombre")
            df = pd.DataFrame(productos, columns=['codigo', 'nombre', 'descripcion', 'precio', 'stock'])
            df.to_excel(file_path, index=False)
            
            messagebox.showinfo("Éxito", f"Productos exportados correctamente a: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar productos: {str(e)}")
    
    @staticmethod
    def importar_clientes_excel(db, callback):
        try:
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo Excel de clientes",
                filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            # Leer el archivo Excel
            df = pd.read_excel(file_path)
            
            # Verificar columnas mínimas requeridas
            required_columns = ['nombre']
            if not all(col in df.columns for col in required_columns):
                messagebox.showerror("Error", f"El archivo debe contener las columnas: {required_columns}")
                return
            
            # Procesar cada fila
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    nombre = str(row['nombre']).strip()
                    if not nombre:
                        continue
                    
                    dni = str(row['dni']).strip() if 'dni' in df.columns and pd.notna(row.get('dni')) else ""
                    direccion = str(row['direccion']).strip() if 'direccion' in df.columns and pd.notna(row.get('direccion')) else ""
                    telefono = str(row['telefono']).strip() if 'telefono' in df.columns and pd.notna(row.get('telefono')) else ""
                    email = str(row['email']).strip() if 'email' in df.columns and pd.notna(row.get('email')) else ""
                    
                    # Verificar si el cliente ya existe
                    existing_client = None
                    if dni:
                        existing_client = db.fetch_one("SELECT id FROM clientes WHERE dni = ?", (dni,))
                    if not existing_client:
                        existing_client = db.fetch_one("SELECT id FROM clientes WHERE nombre = ?", (nombre,))
                    
                    if existing_client:
                        # Actualizar cliente existente
                        db.execute_query(
                            "UPDATE clientes SET dni=?, direccion=?, telefono=?, email=? WHERE id=?",
                            (dni, direccion, telefono, email, existing_client[0])
                        )
                    else:
                        # Insertar nuevo cliente
                        db.execute_query(
                            "INSERT INTO clientes (nombre, dni, direccion, telefono, email) VALUES (?, ?, ?, ?, ?)",
                            (nombre, dni, direccion, telefono, email)
                        )
                    
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"Fila {index + 2}: {str(e)}")
            
            # Mostrar resultados
            message = f"Importación completada:\n- Correctos: {success_count}\n- Errores: {error_count}"
            if errors:
                message += f"\n\nErrores:\n" + "\n".join(errors[:5])
                if error_count > 5:
                    message += f"\n... y {error_count - 5} más"
            
            messagebox.showinfo("Resultado de importación", message)
            callback()  # Actualizar la vista
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar clientes: {str(e)}")
    
    @staticmethod
    def importar_productos_excel(db, callback):
        try:
            file_path = filedialog.askopenfilename(
                title="Seleccionar archivo Excel de productos",
                filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
                
            # Leer el archivo Excel
            df = pd.read_excel(file_path)
            
            # Verificar columnas mínimas requeridas
            required_columns = ['codigo', 'nombre', 'precio']
            if not all(col in df.columns for col in required_columns):
                messagebox.showerror("Error", f"El archivo debe contener las columnas: {required_columns}")
                return
            
            # Procesar cada fila
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    codigo = str(row['codigo']).strip()
                    nombre = str(row['nombre']).strip()
                    precio = float(row['precio'])
                    
                    if not codigo or not nombre:
                        continue
                    
                    descripcion = str(row['descripcion']).strip() if 'descripcion' in df.columns and pd.notna(row.get('descripcion')) else ""
                    stock = int(row['stock']) if 'stock' in df.columns and pd.notna(row.get('stock')) else 0
                    
                    # Verificar si el producto ya existe
                    existing_product = db.fetch_one("SELECT id FROM productos WHERE codigo = ?", (codigo,))
                    
                    if existing_product:
                        # Actualizar producto existente
                        db.execute_query(
                            "UPDATE productos SET nombre=?, descripcion=?, precio=?, stock=? WHERE id=?",
                            (nombre, descripcion, precio, stock, existing_product[0])
                        )
                    else:
                        # Insertar nuevo producto
                        db.execute_query(
                            "INSERT INTO productos (codigo, nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?, ?)",
                            (codigo, nombre, descripcion, precio, stock)
                        )
                    
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"Fila {index + 2}: {str(e)}")
            
            # Mostrar resultados
            message = f"Importación completada:\n- Correctos: {success_count}\n- Errores: {error_count}"
            if errors:
                message += f"\n\nErrores:\n" + "\n".join(errors[:5])
                if error_count > 5:
                    message += f"\n... y {error_count - 5} más"
            
            messagebox.showinfo("Resultado de importación", message)
            callback()  # Actualizar la vista
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar productos: {str(e)}")