from tkinter import ttk, messagebox, simpledialog, filedialog
from database import Database
from models import Cliente, Producto, Factura, DetalleFactura
from invoice_generator import InvoiceGenerator
from datetime import datetime
import pandas as pd, os, tkinter as tk

class FacturacionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Facturación")
        self.root.geometry("1200x700")
        
        self.db = Database()
        self.invoice_gen = InvoiceGenerator()
        
        self.current_factura = None
        self.detalles_temp = []
        self.configuracion = self.cargar_configuracion()
        self.cupon_aplicado = None
        
        self.setup_ui()
        self.load_clientes()
        self.load_productos()

    def abrir_dialogo_cliente_manual(self):
        """Abre diálogo para ingresar datos de cliente manualmente"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Datos del Cliente")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        # Centrar diálogo
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos del formulario
        ttk.Label(dialog, text="Nombre:*").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        nombre_entry = ttk.Entry(dialog, width=30)
        nombre_entry.grid(row=0, column=1, padx=10, pady=10)
        nombre_entry.focus()
        
        ttk.Label(dialog, text="DNI:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        dni_entry = ttk.Entry(dialog, width=30)
        dni_entry.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Dirección:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        direccion_entry = ttk.Entry(dialog, width=30)
        direccion_entry.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Teléfono:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
        telefono_entry = ttk.Entry(dialog, width=30)
        telefono_entry.grid(row=3, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Email:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
        email_entry = ttk.Entry(dialog, width=30)
        email_entry.grid(row=4, column=1, padx=10, pady=10)
        
        # Variable para almacenar el cliente manual
        self.cliente_manual = None
        
        def guardar_cliente_manual():
            nombre = nombre_entry.get().strip()
            dni = dni_entry.get().strip()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            # Crear objeto cliente manual
            self.cliente_manual = Cliente(
                nombre=nombre,
                dni=dni,
                direccion=direccion_entry.get().strip(),
                telefono=telefono_entry.get().strip(),
                email=email_entry.get().strip()
            )
            
            # Actualizar combobox para mostrar el cliente manual
            self.cliente_combobox.set(f"{nombre} (DNI: {dni}) - MANUAL")
            dialog.destroy()
        
        def cancelar():
            dialog.destroy()
        
        # Botones
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Cancelar", command=cancelar).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Usar Cliente", command=guardar_cliente_manual).pack(side='right', padx=10)


    def cargar_configuracion(self):
        """Carga la configuración del sistema desde la base de datos"""
        config_db = self.db.fetch_one("SELECT * FROM configuracion LIMIT 1")
        if config_db:
            return {
                'porcentaje_iva': config_db[1],
                'descuento_efectivo': config_db[2],
                'habilitar_descuento_efectivo': bool(config_db[3]),
                'habilitar_cupones': bool(config_db[4])
            }
        return {
            'porcentaje_iva': 12.0,
            'descuento_efectivo': 5.0,
            'habilitar_descuento_efectivo': True,
            'habilitar_cupones': False
        }
    
    def setup_ui(self):
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de Facturación
        self.frame_facturacion = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_facturacion, text="Facturación")
        
        # Pestaña de Clientes
        self.frame_clientes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_clientes, text="Clientes")
        
        # Pestaña de Productos
        self.frame_productos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_productos, text="Productos")
        
        # Pestaña de Configuración
        self.frame_config = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_config, text="Configuración")
        
        # Pestaña de Cupones
        self.frame_cupones = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_cupones, text="Cupones")
        
        self.setup_facturacion_tab()
        self.setup_clientes_tab()
        self.setup_productos_tab()
        self.setup_config_tab()
        self.setup_cupones_tab()

    def setup_facturacion_tab(self):
        # Frame izquierdo (Selección de cliente y productos)
        left_frame = ttk.Frame(self.frame_facturacion)
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Selección de cliente
        cliente_frame = ttk.Frame(left_frame)
        cliente_frame.pack(fill='x', pady=5)
        
        ttk.Label(cliente_frame, text="Seleccionar Cliente:").pack(anchor='w')
        
        # Frame para combobox y botón
        cliente_select_frame = ttk.Frame(cliente_frame)
        cliente_select_frame.pack(fill='x', pady=5)
        
        self.cliente_combobox = ttk.Combobox(cliente_select_frame, state="readonly", width=30)
        self.cliente_combobox.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        # Botón para cliente manual
        ttk.Button(cliente_select_frame, text="Cliente Manual", 
                command=self.abrir_dialogo_cliente_manual).pack(side='right')
        
        # Lista de productos
        ttk.Label(left_frame, text="Productos Disponibles:").pack(anchor='w', pady=(10,0))
        self.productos_tree = ttk.Treeview(left_frame, columns=('codigo', 'nombre', 'precio', 'stock'), show='headings', height=15)
        self.productos_tree.heading('codigo', text='Código')
        self.productos_tree.heading('nombre', text='Nombre')
        self.productos_tree.heading('precio', text='Precio')
        self.productos_tree.heading('stock', text='Stock')
        self.productos_tree.column('codigo', width=80)
        self.productos_tree.column('nombre', width=150)
        self.productos_tree.column('precio', width=80)
        self.productos_tree.column('stock', width=60)
        self.productos_tree.pack(fill='both', expand=True, pady=5)
        self.productos_tree.bind('<Double-1>', self.agregar_producto_factura)
        
        # Frame derecho (Detalles de factura)
        right_frame = ttk.Frame(self.frame_facturacion)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Método de pago
        payment_frame = ttk.Frame(right_frame)
        payment_frame.pack(fill='x', pady=5)
        
        ttk.Label(payment_frame, text="Método de Pago:").pack(side='left', padx=5)
        self.metodo_pago = tk.StringVar(value="EFECTIVO")
        ttk.Radiobutton(payment_frame, text="Efectivo", variable=self.metodo_pago, value="EFECTIVO", 
                    command=self.calcular_totales).pack(side='left', padx=5)
        ttk.Radiobutton(payment_frame, text="Débito", variable=self.metodo_pago, value="DEBITO",
                    command=self.calcular_totales).pack(side='left', padx=5)
        
        # Cupón de descuento
        if self.configuracion['habilitar_cupones']:
            coupon_frame = ttk.Frame(right_frame)
            coupon_frame.pack(fill='x', pady=5)
            
            ttk.Label(coupon_frame, text="Cupón de descuento:").pack(side='left', padx=5)
            self.cupon_entry = ttk.Entry(coupon_frame, width=15)
            self.cupon_entry.pack(side='left', padx=5)
            ttk.Button(coupon_frame, text="Aplicar", command=self.aplicar_cupon).pack(side='left', padx=5)
            self.cupon_status = ttk.Label(coupon_frame, text="", foreground="green")
            self.cupon_status.pack(side='left', padx=5)
        
        # Detalles de la factura actual
        ttk.Label(right_frame, text="Detalles de Factura:").pack(anchor='w')
        self.detalles_tree = ttk.Treeview(right_frame, columns=('producto', 'cantidad', 'precio', 'total'), show='headings', height=10)
        self.detalles_tree.heading('producto', text='Producto')
        self.detalles_tree.heading('cantidad', text='Cantidad')
        self.detalles_tree.heading('precio', text='Precio Unit.')
        self.detalles_tree.heading('total', text='Total')
        self.detalles_tree.column('producto', width=150)
        self.detalles_tree.column('cantidad', width=80)
        self.detalles_tree.column('precio', width=100)
        self.detalles_tree.column('total', width=100)
        self.detalles_tree.pack(fill='both', expand=True, pady=5)
        
        # Totales
        total_frame = ttk.Frame(right_frame)
        total_frame.pack(fill='x', pady=5)
        
        ttk.Label(total_frame, text="Subtotal:").grid(row=0, column=0, sticky='e', padx=5)
        self.subtotal_var = tk.StringVar(value="$0.00")
        ttk.Label(total_frame, textvariable=self.subtotal_var).grid(row=0, column=1, sticky='w', padx=5)
        
        # Hacer la etiqueta de IVA accesible
        self.iva_label = ttk.Label(total_frame, text=f"IVA ({self.configuracion['porcentaje_iva']}%):")
        self.iva_label.grid(row=1, column=0, sticky='e', padx=5)
        
        self.iva_var = tk.StringVar(value="$0.00")
        ttk.Label(total_frame, textvariable=self.iva_var).grid(row=1, column=1, sticky='w', padx=5)
        
        ttk.Label(total_frame, text="Descuento:").grid(row=2, column=0, sticky='e', padx=5)
        self.descuento_var = tk.StringVar(value="$0.00")
        ttk.Label(total_frame, textvariable=self.descuento_var).grid(row=2, column=1, sticky='w', padx=5)
        
        ttk.Label(total_frame, text="Total:").grid(row=3, column=0, sticky='e', padx=5)
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(total_frame, textvariable=self.total_var, font=('Arial', 12, 'bold')).grid(row=3, column=1, sticky='w', padx=5)
        
        # Botones
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Generar Factura", command=self.generar_factura).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_factura).pack(side='right', padx=5)

    
    def setup_config_tab(self):
        """Configura la pestaña de configuración del sistema"""
        # Configuración de IVA
        iva_frame = ttk.LabelFrame(self.frame_config, text="Configuración de IVA")
        iva_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(iva_frame, text="Porcentaje de IVA (%):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.iva_entry = ttk.Entry(iva_frame, width=10)
        self.iva_entry.insert(0, str(self.configuracion['porcentaje_iva']))
        self.iva_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Configuración de descuentos
        descuento_frame = ttk.LabelFrame(self.frame_config, text="Configuración de Descuentos")
        descuento_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(descuento_frame, text="Descuento por pago en efectivo (%):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.descuento_efectivo_entry = ttk.Entry(descuento_frame, width=10)
        self.descuento_efectivo_entry.insert(0, str(self.configuracion['descuento_efectivo']))
        self.descuento_efectivo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.habilitar_descuento_var = tk.BooleanVar(value=self.configuracion['habilitar_descuento_efectivo'])
        ttk.Checkbutton(descuento_frame, text="Habilitar descuento por pago en efectivo", 
                       variable=self.habilitar_descuento_var).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        
        self.habilitar_cupones_var = tk.BooleanVar(value=self.configuracion['habilitar_cupones'])
        ttk.Checkbutton(descuento_frame, text="Habilitar sistema de cupones", 
                       variable=self.habilitar_cupones_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        
        # Botón guardar configuración
        ttk.Button(self.frame_config, text="Guardar Configuración", command=self.guardar_configuracion).pack(pady=10)
    
    def setup_cupones_tab(self):
        """Configura la pestaña de gestión de cupones"""
        if not self.configuracion['habilitar_cupones']:
            ttk.Label(self.frame_cupones, text="Los cupones están deshabilitados en la configuración").pack(pady=20)
            return
        
        # Treeview para cupones
        columns = ('id', 'codigo', 'descuento', 'valido_desde', 'valido_hasta', 'usos_maximos', 'usos_actuales', 'activo')
        self.cupones_tree = ttk.Treeview(self.frame_cupones, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.cupones_tree.heading(col, text=col.capitalize())
            self.cupones_tree.column(col, width=100)
        
        self.cupones_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botones para cupones
        button_frame = ttk.Frame(self.frame_cupones)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Agregar Cupón", command=self.agregar_cupon).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Editar Cupón", command=self.editar_cupon).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Eliminar Cupón", command=self.eliminar_cupon).pack(side='left', padx=5)
        
        self.load_cupones()
    
    def guardar_configuracion(self):
        """Guarda la configuración del sistema"""
        try:
            iva = float(self.iva_entry.get())
            descuento_efectivo = float(self.descuento_efectivo_entry.get())
            
            # Actualizar configuración en memoria
            self.configuracion = {
                'porcentaje_iva': iva,
                'descuento_efectivo': descuento_efectivo,
                'habilitar_descuento_efectivo': self.habilitar_descuento_var.get(),
                'habilitar_cupones': self.habilitar_cupones_var.get()
            }
            
            # Guardar en base de datos
            self.db.execute_query("DELETE FROM configuracion")
            self.db.execute_query(
                "INSERT INTO configuracion (porcentaje_iva, descuento_efectivo, habilitar_descuento_efectivo, habilitar_cupones) VALUES (?, ?, ?, ?)",
                (iva, descuento_efectivo, int(self.habilitar_descuento_var.get()), int(self.habilitar_cupones_var.get()))
            )
            
            # ACTUALIZACIONES CRÍTICAS QUE FALTABAN:
            
            # 1. Actualizar etiqueta de IVA en la pestaña de facturación
            self.iva_label.config(text=f"IVA ({iva}%):")  # ← AQUÍ VA LA LÍNEA
            
            # 2. Actualizar pestaña de cupones si cambió el estado
            if self.configuracion['habilitar_cupones']:
                # Habilitar funcionalidad de cupones
                if hasattr(self, 'cupon_entry'):
                    self.cupon_entry.config(state='normal')
                if hasattr(self, 'cupon_status'):
                    self.cupon_status.config(text="")
            else:
                # Deshabilitar funcionalidad de cupones
                if hasattr(self, 'cupon_entry'):
                    self.cupon_entry.config(state='disabled')
                if hasattr(self, 'cupon_status'):
                    self.cupon_status.config(text="Cupones deshabilitados", foreground="red")
                self.cupon_aplicado = None
            
            # 3. Recalcular totales de la factura actual
            self.calcular_totales()
            
            # 4. Recargar la pestaña de cupones si es necesario
            if hasattr(self, 'frame_cupones'):
                # Destruir el frame actual y recrearlo
                for widget in self.frame_cupones.winfo_children():
                    widget.destroy()
                self.setup_cupones_tab()

            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "Los valores de IVA y descuento deben ser números válidos")
    
    def aplicar_cupon(self):
        """Aplica un cupón de descuento a la factura actual"""
        if not self.configuracion['habilitar_cupones']:
            messagebox.showerror("Error", "Los cupones están deshabilitados")
            return
        
        codigo = self.cupon_entry.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese un código de cupón")
            return
        
        # Verificar el cupón en la base de datos
        cupon_db = self.db.fetch_one("SELECT * FROM cupones WHERE codigo = ? AND activo = 1", (codigo,))
        if not cupon_db:
            self.cupon_status.config(text="Cupón inválido", foreground="red")
            return
        
        # Verificar fechas de validez
        hoy = datetime.now().strftime("%Y-%m-%d")
        if cupon_db[3] and hoy < cupon_db[3]:
            self.cupon_status.config(text="Cupón aún no válido", foreground="red")
            return
        
        if cupon_db[4] and hoy > cupon_db[4]:
            self.cupon_status.config(text="Cupón expirado", foreground="red")
            return
        
        # Verificar usos máximos
        if cupon_db[5] > 0 and cupon_db[6] >= cupon_db[5]:
            self.cupon_status.config(text="Cupón sin usos disponibles", foreground="red")
            return
        
        # Cupón válido
        self.cupon_aplicado = {
            'id': cupon_db[0],
            'codigo': cupon_db[1],
            'descuento': cupon_db[2]
        }
        
        self.cupon_status.config(text=f"Descuento: {cupon_db[2]}% aplicado", foreground="green")
        self.calcular_totales()
    
    def load_cupones(self):
        """Carga los cupones desde la base de datos"""
        cupones = self.db.fetch_all("SELECT * FROM cupones ORDER BY codigo")
        
        for item in self.cupones_tree.get_children():
            self.cupones_tree.delete(item)
        
        for cupon in cupones:
            self.cupones_tree.insert('', 'end', values=cupon)
    
    def agregar_cupon(self):
        self.abrir_dialogo_cupon()
    
    def editar_cupon(self):
        selection = self.cupones_tree.selection()
        if selection:
            item = self.cupones_tree.item(selection[0])
            self.abrir_dialogo_cupon(item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un cupón para editar")
    
    def abrir_dialogo_cupon(self, cupon_data=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Cupón" if not cupon_data else "Editar Cupón")
        dialog.geometry("400x400")
        
        # Campos del formulario
        ttk.Label(dialog, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        codigo_entry = ttk.Entry(dialog, width=30)
        codigo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Descuento (%):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        descuento_entry = ttk.Entry(dialog, width=30)
        descuento_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Válido desde:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        valido_desde_entry = ttk.Entry(dialog, width=30)
        valido_desde_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Formato: YYYY-MM-DD").grid(row=3, column=1, padx=5, sticky='w')
        
        ttk.Label(dialog, text="Válido hasta:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        valido_hasta_entry = ttk.Entry(dialog, width=30)
        valido_hasta_entry.grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(dialog, text="Formato: YYYY-MM-DD").grid(row=5, column=1, padx=5, sticky='w')
        
        ttk.Label(dialog, text="Usos máximos:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
        usos_maximos_entry = ttk.Entry(dialog, width=30)
        usos_maximos_entry.grid(row=6, column=1, padx=5, pady=5)
        
        activo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(dialog, text="Activo", variable=activo_var).grid(row=7, column=1, padx=5, pady=5, sticky='w')
        
        # Llenar campos si es edición
        if cupon_data:
            codigo_entry.insert(0, cupon_data[1])
            descuento_entry.insert(0, str(cupon_data[2]))
            valido_desde_entry.insert(0, cupon_data[3] or "")
            valido_hasta_entry.insert(0, cupon_data[4] or "")
            usos_maximos_entry.insert(0, str(cupon_data[5]))
            activo_var.set(bool(cupon_data[7]))
        
        def guardar_cupon():
            codigo = codigo_entry.get().strip()
            descuento = descuento_entry.get().strip()
            
            if not all([codigo, descuento]):
                messagebox.showerror("Error", "Código y descuento son obligatorios")
                return
            
            try:
                descuento_val = float(descuento)
                usos_maximos_val = int(usos_maximos_entry.get()) if usos_maximos_entry.get() else 1
                
                if cupon_data:  # Edición
                    self.db.execute_query(
                        "UPDATE cupones SET codigo=?, descuento=?, valido_desde=?, valido_hasta=?, usos_maximos=?, activo=? WHERE id=?",
                        (codigo, descuento_val, valido_desde_entry.get() or None, valido_hasta_entry.get() or None, 
                         usos_maximos_val, int(activo_var.get()), cupon_data[0])
                    )
                else:  # Inserción
                    self.db.execute_query(
                        "INSERT INTO cupones (codigo, descuento, valido_desde, valido_hasta, usos_maximos, activo) VALUES (?, ?, ?, ?, ?, ?)",
                        (codigo, descuento_val, valido_desde_entry.get() or None, valido_hasta_entry.get() or None, 
                         usos_maximos_val, int(activo_var.get()))
                    )
                
                self.load_cupones()
                dialog.destroy()
                messagebox.showinfo("Éxito", "Cupón guardado correctamente")
                
            except ValueError:
                messagebox.showerror("Error", "Descuento y usos máximos deben ser números válidos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar cupón: {str(e)}")
        
        ttk.Button(dialog, text="Guardar", command=guardar_cupon).grid(row=8, column=1, pady=10)
    
    def eliminar_cupon(self):
        selection = self.cupones_tree.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cupón?"):
                item = self.cupones_tree.item(selection[0])
                try:
                    self.db.execute_query("DELETE FROM cupones WHERE id = ?", (item['values'][0],))
                    self.load_cupones()
                    messagebox.showinfo("Éxito", "Cupón eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar cupón: {str(e)}")
        else:
            messagebox.showerror("Error", "Seleccione un cupón para eliminar")

    def setup_clientes_tab(self):
        # Treeview para clientes (cambiado RUC por DNI)
        columns = ('id', 'nombre', 'dni', 'direccion', 'telefono', 'email')
        self.clientes_tree = ttk.Treeview(self.frame_clientes, columns=columns, show='headings')
        
        for col in columns:
            self.clientes_tree.heading(col, text=col.capitalize())
            self.clientes_tree.column(col, width=100)
        
        self.clientes_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botones para clientes - CON BOTÓN DE IMPORTACIÓN
        button_frame = ttk.Frame(self.frame_clientes)
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


    def setup_productos_tab(self):
        # Treeview para productos
        columns = ('id', 'codigo', 'nombre', 'descripcion', 'precio', 'stock')
        self.productos_tree_tab = ttk.Treeview(self.frame_productos, columns=columns, show='headings')
        
        for col in columns:
            self.productos_tree_tab.heading(col, text=col.capitalize())
            self.productos_tree_tab.column(col, width=100)
        
        self.productos_tree_tab.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botones para productos - CON BOTÓN DE IMPORTACIÓN
        button_frame = ttk.Frame(self.frame_productos)
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


    def exportar_clientes_excel(self):
        """Exporta clientes a Excel"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Guardar clientes como Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
            
            clientes = self.db.fetch_all("SELECT nombre, dni, direccion, telefono, email FROM clientes ORDER BY nombre")
            
            df = pd.DataFrame(clientes, columns=['nombre', 'dni', 'direccion', 'telefono', 'email'])
            df.to_excel(file_path, index=False)
            
            messagebox.showinfo("Éxito", f"Clientes exportados correctamente a: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar clientes: {str(e)}")

    def exportar_productos_excel(self):
        """Exporta productos a Excel"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Guardar productos como Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if not file_path:
                return
            
            productos = self.db.fetch_all("SELECT codigo, nombre, descripcion, precio, stock FROM productos ORDER BY nombre")
            
            df = pd.DataFrame(productos, columns=['codigo', 'nombre', 'descripcion', 'precio', 'stock'])
            df.to_excel(file_path, index=False)
            
            messagebox.showinfo("Éxito", f"Productos exportados correctamente a: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar productos: {str(e)}")



    def importar_clientes_excel(self):
        """Importa clientes desde un archivo Excel"""
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
                        existing_client = self.db.fetch_one("SELECT id FROM clientes WHERE dni = ?", (dni,))
                    if not existing_client:
                        existing_client = self.db.fetch_one("SELECT id FROM clientes WHERE nombre = ?", (nombre,))
                    
                    if existing_client:
                        # Actualizar cliente existente
                        self.db.execute_query(
                            "UPDATE clientes SET dni=?, direccion=?, telefono=?, email=? WHERE id=?",
                            (dni, direccion, telefono, email, existing_client[0])
                        )
                    else:
                        # Insertar nuevo cliente
                        self.db.execute_query(
                            "INSERT INTO clientes (nombre, dni, direccion, telefono, email) VALUES (?, ?, ?, ?, ?)",
                            (nombre, dni, direccion, telefono, email)
                        )
                    
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"Fila {index + 2}: {str(e)}")
            
            # Actualizar la lista de clientes
            self.load_clientes()
            
            # Mostrar resultados
            message = f"Importación completada:\n- Correctos: {success_count}\n- Errores: {error_count}"
            if errors:
                message += f"\n\nErrores:\n" + "\n".join(errors[:5])  # Mostrar solo primeros 5 errores
                if error_count > 5:
                    message += f"\n... y {error_count - 5} más"
            
            messagebox.showinfo("Resultado de importación", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar clientes: {str(e)}")

    def importar_productos_excel(self):
        """Importa productos desde un archivo Excel"""
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
                    existing_product = self.db.fetch_one("SELECT id FROM productos WHERE codigo = ?", (codigo,))
                    
                    if existing_product:
                        # Actualizar producto existente
                        self.db.execute_query(
                            "UPDATE productos SET nombre=?, descripcion=?, precio=?, stock=? WHERE id=?",
                            (nombre, descripcion, precio, stock, existing_product[0])
                        )
                    else:
                        # Insertar nuevo producto
                        self.db.execute_query(
                            "INSERT INTO productos (codigo, nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?, ?)",
                            (codigo, nombre, descripcion, precio, stock)
                        )
                    
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f"Fila {index + 2}: {str(e)}")
            
            # Actualizar la lista de productos
            self.load_productos()
            
            # Mostrar resultados
            message = f"Importación completada:\n- Correctos: {success_count}\n- Errores: {error_count}"
            if errors:
                message += f"\n\nErrores:\n" + "\n".join(errors[:5])  # Mostrar solo primeros 5 errores
                if error_count > 5:
                    message += f"\n... y {error_count - 5} más"
            
            messagebox.showinfo("Resultado de importación", message)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar productos: {str(e)}")


    def load_clientes(self):
        # Cargar clientes en el combobox y treeview (cambiado RUC por DNI)
        clientes = self.db.fetch_all("SELECT id, nombre, dni, direccion, telefono, email FROM clientes ORDER BY nombre")
        self.cliente_combobox['values'] = [f"{c[1]} (DNI: {c[2]})" for c in clientes]
        
        # Limpiar y cargar treeview de clientes
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        for cliente in clientes:
            self.clientes_tree.insert('', 'end', values=cliente)
    
    def load_productos(self):
        # Cargar productos en el treeview de facturación
        productos = self.db.fetch_all("SELECT * FROM productos ORDER BY nombre")
        
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        for producto in productos:
            # Asegurar que el stock sea un entero
            stock = producto[5]  # stock está en la posición 5
            try:
                stock_int = int(float(stock))  # Convertir a float primero y luego a int
            except (ValueError, TypeError):
                stock_int = 0
            
            # Insertar en el treeview con valores convertidos
            self.productos_tree.insert('', 'end', values=(
                producto[1],  # codigo
                producto[2],  # nombre
                f"${float(producto[4]):.2f}",  # precio (convertido a float y formateado)
                stock_int     # stock (convertido a entero)
            ))
        
        # Cargar productos en el treeview de la pestaña productos
        for item in self.productos_tree_tab.get_children():
            self.productos_tree_tab.delete(item)
        
        for producto in productos:
            self.productos_tree_tab.insert('', 'end', values=producto)
    
    def agregar_producto_factura(self, event):
        selection = self.productos_tree.selection()
        if selection:
            item = self.productos_tree.item(selection[0])
            valores = item['values']
            
            # Verificar si el producto ya está en la factura
            for detalle in self.detalles_temp:
                if detalle.producto.codigo == valores[0]:
                    messagebox.showinfo("Información", "Este producto ya está en la factura")
                    return
            
            # Convertir stock a entero de manera segura
            try:
                stock_disponible = int(float(valores[3]))  # Convertir a float primero
            except (ValueError, TypeError):
                messagebox.showerror("Error", f"Stock no válido: {valores[3]}")
                return
            
            # Convertir precio a float de manera segura
            try:
                # Remover el símbolo $ si está presente
                precio_str = valores[2].replace('$', '') if isinstance(valores[2], str) else str(valores[2])
                precio = float(precio_str)
            except (ValueError, TypeError):
                messagebox.showerror("Error", f"Precio no válido: {valores[2]}")
                return
            
            # Pedir cantidad
            cantidad = simpledialog.askinteger(
                "Cantidad", 
                f"Ingrese cantidad para {valores[1]} (Stock disponible: {stock_disponible}):", 
                minvalue=1,
                maxvalue=stock_disponible  # Limitar máximo al stock disponible
            )
            
            if cantidad and cantidad > 0:
                if cantidad > stock_disponible:
                    messagebox.showerror("Error", f"Stock insuficiente. Disponible: {stock_disponible}")
                    return
                
                total_linea = precio * cantidad
                
                # Agregar a detalles temporales
                producto = Producto(codigo=valores[0], nombre=valores[1], precio=precio)
                detalle = DetalleFactura(
                    producto=producto, 
                    cantidad=cantidad, 
                    precio_unitario=precio, 
                    total_linea=total_linea
                )
                self.detalles_temp.append(detalle)
                
                # Agregar al treeview
                self.detalles_tree.insert('', 'end', values=(
                    producto.nombre, 
                    cantidad, 
                    f"${precio:.2f}", 
                    f"${total_linea:.2f}"
                ))
                
                self.calcular_totales()
    
    def calcular_totales(self):
        subtotal = sum(detalle.total_linea for detalle in self.detalles_temp)
        
        # Calcular descuentos
        descuento = 0
        
        # Descuento por pago en efectivo
        if (self.metodo_pago.get() == "EFECTIVO" and 
            self.configuracion['habilitar_descuento_efectivo']):
            descuento += subtotal * (self.configuracion['descuento_efectivo'] / 100)
        
        # Descuento por cupón
        if self.cupon_aplicado:
            descuento += subtotal * (self.cupon_aplicado['descuento'] / 100)
        
        # Calcular base imponible
        base_imponible = subtotal - descuento
        
        # Calcular IVA
        iva = base_imponible * (self.configuracion['porcentaje_iva'] / 100)
        total = base_imponible + iva
        
        self.subtotal_var.set(f"${subtotal:.2f}")
        self.descuento_var.set(f"${descuento:.2f}")
        self.iva_var.set(f"${iva:.2f}")
        self.total_var.set(f"${total:.2f}")


    def generar_factura(self):
        if not self.detalles_temp:
            messagebox.showerror("Error", "Debe agregar productos a la factura")
            return
        
        cliente_selection = self.cliente_combobox.get()
        if not cliente_selection:
            messagebox.showerror("Error", "Debe seleccionar un cliente")
            return
        
        try:
            # Verificar si es cliente manual
            if hasattr(self, 'cliente_manual') and self.cliente_manual and "MANUAL" in cliente_selection:
                cliente_obj = self.cliente_manual
                cliente_obj.id = None  # Importante para que el template detecte que es manual
                cliente_id = None
            else:
                # Obtener ID del cliente desde la selección
                cliente_nombre = cliente_selection.split(' (DNI:')[0].strip()
                
                # Buscar cliente por nombre
                cliente = self.db.fetch_one("SELECT id, nombre, dni, direccion, telefono, email FROM clientes WHERE nombre = ?", (cliente_nombre,))
                
                if not cliente:
                    # Intentar buscar por DNI si no se encuentra por nombre
                    try:
                        dni = cliente_selection.split('(DNI:')[1].replace(')', '').strip()
                        cliente = self.db.fetch_one("SELECT id, nombre, dni, direccion, telefono, email FROM clientes WHERE dni = ?", (dni,))
                    except:
                        cliente = None
                
                if not cliente:
                    messagebox.showerror("Error", "Cliente no encontrado en la base de datos")
                    return
                
                cliente_id = cliente[0]
                cliente_obj = Cliente(
                    id=cliente[0], 
                    nombre=cliente[1], 
                    dni=cliente[2],
                    direccion=cliente[3], 
                    telefono=cliente[4], 
                    email=cliente[5]
                )
            
            # Crear número de factura único
            numero_factura = f"FACT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Calcular totales
            subtotal = sum(detalle.total_linea for detalle in self.detalles_temp)
            
            # Calcular descuentos
            descuento = 0
            if (self.metodo_pago.get() == "EFECTIVO" and 
                self.configuracion['habilitar_descuento_efectivo']):
                descuento += subtotal * (self.configuracion['descuento_efectivo'] / 100)
            
            if self.cupon_aplicado:
                descuento += subtotal * (self.cupon_aplicado['descuento'] / 100)
            
            # Calcular base imponible
            base_imponible = subtotal - descuento
            
            # Calcular IVA
            iva = base_imponible * (self.configuracion['porcentaje_iva'] / 100)
            total = base_imponible + iva
            
            # Insertar factura (con método de pago y descuento)
            # Para cliente manual, usar cliente_id como NULL
            self.db.execute_query(
                "INSERT INTO facturas (numero_factura, fecha, cliente_id, subtotal, descuento, iva, total, metodo_pago) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (numero_factura, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cliente_id, subtotal, descuento, iva, total, self.metodo_pago.get())
            )
            
            # Obtener ID de la factura insertada
            factura_id_result = self.db.fetch_one("SELECT last_insert_rowid()")
            if not factura_id_result:
                raise Exception("No se pudo obtener el ID de la factura insertada")
            
            factura_id = factura_id_result[0]
            
            # Insertar detalles
            for detalle in self.detalles_temp:
                # Buscar producto por código como texto
                producto_db = self.db.fetch_one("SELECT id FROM productos WHERE codigo = ?", (str(detalle.producto.codigo),))
                
                if not producto_db:
                    # Intentar buscar por nombre si no se encuentra por código
                    producto_db = self.db.fetch_one("SELECT id FROM productos WHERE nombre = ?", (detalle.producto.nombre,))
                    
                if not producto_db:
                    raise Exception(f"Producto '{detalle.producto.nombre}' (código: {detalle.producto.codigo}) no encontrado en la base de datos")
                
                producto_id = producto_db[0]
                
                self.db.execute_query(
                    "INSERT INTO detalles_factura (factura_id, producto_id, cantidad, precio_unitario, total_linea) VALUES (?, ?, ?, ?, ?)",
                    (factura_id, producto_id, detalle.cantidad, detalle.precio_unitario, detalle.total_linea)
                )
                
                # Actualizar stock (disminuir)
                self.db.execute_query(
                    "UPDATE productos SET stock = stock - ? WHERE id = ?",
                    (detalle.cantidad, producto_id)
                )
            
            # Actualizar uso de cupón si se aplicó
            if self.cupon_aplicado:
                self.db.execute_query(
                    "UPDATE cupones SET usos_actuales = usos_actuales + 1 WHERE id = ?",
                    (self.cupon_aplicado['id'],)
                )

            # Generar PDF
            factura_obj = Factura(
                id=factura_id,
                numero_factura=numero_factura,
                fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                cliente=cliente_obj,
                detalles=self.detalles_temp,
                subtotal=subtotal,
                descuento=descuento,
                iva=iva,
                total=total,
                metodo_pago=self.metodo_pago.get()
            )
            
            pdf_path = self.invoice_gen.generate_invoice(factura_obj)
            
            messagebox.showinfo("Éxito", f"Factura generada exitosamente\nGuardada en: {pdf_path}")
            self.limpiar_factura()
            self.load_productos()  # Actualizar stock en la interfaz
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar factura: {str(e)}")
            # Para debugging, puedes imprimir el traceback completo
            import traceback
            print(traceback.format_exc())

    def limpiar_factura(self):
        self.detalles_temp = []
        for item in self.detalles_tree.get_children():
            self.detalles_tree.delete(item)
        self.calcular_totales()
        self.cliente_combobox.set('')
        self.metodo_pago.set("EFECTIVO")
        self.cupon_aplicado = None
        
        # Limpiar cliente manual si existe
        if hasattr(self, 'cliente_manual'):
            self.cliente_manual = None
        
        if hasattr(self, 'cupon_entry'):
            self.cupon_entry.delete(0, tk.END)
        if hasattr(self, 'cupon_status'):
            self.cupon_status.config(text="")

    
    def agregar_cliente(self):
        self.abrir_dialogo_cliente()
    
    def editar_cliente(self):
        selection = self.clientes_tree.selection()
        if selection:
            item = self.clientes_tree.item(selection[0])
            self.abrir_dialogo_cliente(item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un cliente para editar")
    
    def abrir_dialogo_cliente(self, cliente_data=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar/Editar Cliente" if not cliente_data else "Editar Cliente")
        dialog.geometry("400x300")
        
        # Campos del formulario (cambiado RUC por DNI)
        ttk.Label(dialog, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        nombre_entry = ttk.Entry(dialog, width=30)
        nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="DNI:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        dni_entry = ttk.Entry(dialog, width=30)
        dni_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Dirección:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        direccion_entry = ttk.Entry(dialog, width=30)
        direccion_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        telefono_entry = ttk.Entry(dialog, width=30)
        telefono_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Email:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        email_entry = ttk.Entry(dialog, width=30)
        email_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Llenar campos si es edición
        if cliente_data:
            nombre_entry.insert(0, cliente_data[1])
            dni_entry.insert(0, cliente_data[2])  # Cambiado de ruc a dni
            direccion_entry.insert(0, cliente_data[3])
            telefono_entry.insert(0, cliente_data[4])
            email_entry.insert(0, cliente_data[5])
        
        def guardar_cliente():
            nombre = nombre_entry.get().strip()
            dni = dni_entry.get().strip()  # Cambiado de ruc a dni
            
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
            
            try:
                if cliente_data:  # Edición
                    self.db.execute_query(
                        "UPDATE clientes SET nombre=?, dni=?, direccion=?, telefono=?, email=? WHERE id=?",  # Cambiado ruc por dni
                        (nombre, dni, direccion_entry.get(), telefono_entry.get(), email_entry.get(), cliente_data[0])
                    )
                else:  # Inserción
                    self.db.execute_query(
                        "INSERT INTO clientes (nombre, dni, direccion, telefono, email) VALUES (?, ?, ?, ?, ?)",  # Cambiado ruc por dni
                        (nombre, dni, direccion_entry.get(), telefono_entry.get(), email_entry.get())
                    )
                
                self.load_clientes()
                dialog.destroy()
                messagebox.showinfo("Éxito", "Cliente guardado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar cliente: {str(e)}")
        
        ttk.Button(dialog, text="Guardar", command=guardar_cliente).grid(row=5, column=1, pady=10)
    
    def eliminar_cliente(self):
        selection = self.clientes_tree.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
                item = self.clientes_tree.item(selection[0])
                try:
                    self.db.execute_query("DELETE FROM clientes WHERE id = ?", (item['values'][0],))
                    self.load_clientes()
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar cliente: {str(e)}")
        else:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")
    
    def agregar_producto(self):
        self.abrir_dialogo_producto()
    
    def editar_producto(self):
        selection = self.productos_tree_tab.selection()
        if selection:
            item = self.productos_tree_tab.item(selection[0])
            self.abrir_dialogo_producto(item['values'])
        else:
            messagebox.showerror("Error", "Seleccione un producto para editar")
    
    def abrir_dialogo_producto(self, producto_data=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar/Editar Producto" if not producto_data else "Editar Producto")
        dialog.geometry("400x350")
        
        # Campos del formulario
        ttk.Label(dialog, text="Código:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        codigo_entry = ttk.Entry(dialog, width=30)
        codigo_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        nombre_entry = ttk.Entry(dialog, width=30)
        nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Descripción:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        descripcion_entry = ttk.Entry(dialog, width=30)
        descripcion_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Precio:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        precio_entry = ttk.Entry(dialog, width=30)
        precio_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Stock:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        stock_entry = ttk.Entry(dialog, width=30)
        stock_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Llenar campos si es edición
        if producto_data:
            codigo_entry.insert(0, producto_data[1])
            nombre_entry.insert(0, producto_data[2])
            descripcion_entry.insert(0, producto_data[3])
            precio_entry.insert(0, str(producto_data[4]))
            stock_entry.insert(0, str(producto_data[5]))
        
        def guardar_producto():
            codigo = codigo_entry.get().strip()
            nombre = nombre_entry.get().strip()
            precio = precio_entry.get().strip()
            stock = stock_entry.get().strip()
            
            if not all([codigo, nombre, precio]):
                messagebox.showerror("Error", "Código, nombre y precio son obligatorios")
                return
            
            try:
                precio_val = float(precio)
                stock_val = int(stock) if stock else 0
                
                if producto_data:  # Edición
                    self.db.execute_query(
                        "UPDATE productos SET codigo=?, nombre=?, descripcion=?, precio=?, stock=? WHERE id=?",
                        (codigo, nombre, descripcion_entry.get(), precio_val, stock_val, producto_data[0])
                    )
                else:  # Inserción
                    self.db.execute_query(
                        "INSERT INTO productos (codigo, nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?, ?)",
                        (codigo, nombre, descripcion_entry.get(), precio_val, stock_val)
                    )
                
                self.load_productos()
                dialog.destroy()
                messagebox.showinfo("Éxito", "Producto guardado correctamente")
                
            except ValueError:
                messagebox.showerror("Error", "Precio y stock deben ser números válidos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar producto: {str(e)}")
        
        ttk.Button(dialog, text="Guardar", command=guardar_producto).grid(row=5, column=1, pady=10)
    
    def eliminar_producto(self):
        selection = self.productos_tree_tab.selection()
        if selection:
            if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
                item = self.productos_tree_tab.item(selection[0])
                try:
                    self.db.execute_query("DELETE FROM productos WHERE id = ?", (item['values'][0],))
                    self.load_productos()
                    messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
        else:
            messagebox.showerror("Error", "Seleccione un producto para eliminar")



if __name__ == "__main__":
    root = tk.Tk()
    app = FacturacionApp(root)
    root.mainloop()