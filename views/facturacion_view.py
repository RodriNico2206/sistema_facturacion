# views/facturacion_view.py
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from models import Producto, DetalleFactura
from dialogs.cliente_manual_dialog import ClienteManualDialog

class FacturacionView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Frame izquierdo (Selección de cliente y productos)
        left_frame = ttk.Frame(self.frame)
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
        right_frame = ttk.Frame(self.frame)
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
        if self.app.get_config()['habilitar_cupones']:
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
        self.iva_label = ttk.Label(total_frame, text=f"IVA ({self.app.get_config()['porcentaje_iva']}%):")
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
    
    def abrir_dialogo_cliente_manual(self):
        """Abre diálogo para ingresar datos de cliente manualmente"""
        ClienteManualDialog(self.frame, self.app, self.cliente_combobox)
    
    def agregar_producto_factura(self, event):
        selection = self.productos_tree.selection()
        if selection:
            item = self.productos_tree.item(selection[0])
            valores = item['values']
            
            # Verificar si el producto ya está en la factura
            for detalle in self.app.detalles_temp:
                if detalle.producto.codigo == valores[0]:
                    messagebox.showinfo("Información", "Este producto ya está en la factura")
                    return
            
            # Convertir stock a entero de manera segura
            try:
                stock_disponible = int(float(valores[3]))
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
                maxvalue=stock_disponible
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
                self.app.detalles_temp.append(detalle)
                
                # Agregar al treeview
                self.detalles_tree.insert('', 'end', values=(
                    producto.nombre, 
                    cantidad, 
                    f"${precio:.2f}", 
                    f"${total_linea:.2f}"
                ))
                
                self.calcular_totales()
    
    def calcular_totales(self):
        subtotal = sum(detalle.total_linea for detalle in self.app.detalles_temp)
        
        # Calcular descuentos
        descuento = 0
        
        # Descuento por pago en efectivo
        config = self.app.get_config()
        if (self.metodo_pago.get() == "EFECTIVO" and 
            config['habilitar_descuento_efectivo']):
            descuento += subtotal * (config['descuento_efectivo'] / 100)
        
        # Descuento por cupón
        if self.app.cupon_aplicado:
            descuento += subtotal * (self.app.cupon_aplicado['descuento'] / 100)
        
        # Calcular base imponible
        base_imponible = subtotal - descuento
        
        # Calcular IVA
        iva = base_imponible * (config['porcentaje_iva'] / 100)
        total = base_imponible + iva
        
        self.subtotal_var.set(f"${subtotal:.2f}")
        self.descuento_var.set(f"${descuento:.2f}")
        self.iva_var.set(f"${iva:.2f}")
        self.total_var.set(f"${total:.2f}")

    def aplicar_cupon(self):
        """Aplica un cupón de descuento a la factura actual"""
        if not self.app.get_config()['habilitar_cupones']:
            messagebox.showerror("Error", "Los cupones están deshabilitados")
            return
        
        codigo = self.cupon_entry.get().strip()
        if not codigo:
            messagebox.showerror("Error", "Ingrese un código de cupón")
            return
        
        # Verificar el cupón en la base de datos
        cupon_db = self.app.get_db().fetch_one("SELECT * FROM cupones WHERE codigo = ? AND activo = 1", (codigo,))
        if not cupon_db:
            self.cupon_status.config(text="Cupón inválido", foreground="red")
            return
        
        # Verificar fechas de validez
        from datetime import datetime
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
        self.app.cupon_aplicado = {
            'id': cupon_db[0],
            'codigo': cupon_db[1],
            'descuento': cupon_db[2]
        }
        
        self.cupon_status.config(text=f"Descuento: {cupon_db[2]}% aplicado", foreground="green")
        self.calcular_totales()
    
    def generar_factura(self):
        if not self.app.detalles_temp:
            messagebox.showerror("Error", "Debe agregar productos a la factura")
            return
        
        cliente_selection = self.cliente_combobox.get()
        if not cliente_selection:
            messagebox.showerror("Error", "Debe seleccionar un cliente")
            return
        
        try:
            # Verificar si es cliente manual
            if hasattr(self.app, 'cliente_manual') and self.app.cliente_manual and "MANUAL" in cliente_selection:
                cliente_obj = self.app.cliente_manual
                cliente_obj.id = None
                cliente_id = None
            else:
                # Obtener ID del cliente desde la selección
                cliente_nombre = cliente_selection.split(' (DNI:')[0].strip()
                
                # Buscar cliente por nombre
                cliente = self.app.get_db().fetch_one("SELECT id, nombre, dni, direccion, telefono, email FROM clientes WHERE nombre = ?", (cliente_nombre,))
                
                if not cliente:
                    # Intentar buscar por DNI si no se encuentra por nombre
                    try:
                        dni = cliente_selection.split('(DNI:')[1].replace(')', '').strip()
                        cliente = self.app.get_db().fetch_one("SELECT id, nombre, dni, direccion, telefono, email FROM clientes WHERE dni = ?", (dni,))
                    except:
                        cliente = None
                
                if not cliente:
                    messagebox.showerror("Error", "Cliente no encontrado en la base de datos")
                    return
                
                cliente_id = cliente[0]
                from models import Cliente
                cliente_obj = Cliente(
                    id=cliente[0], 
                    nombre=cliente[1], 
                    dni=cliente[2],
                    direccion=cliente[3], 
                    telefono=cliente[4], 
                    email=cliente[5]
                )
            
            # Crear número de factura único
            from datetime import datetime
            numero_factura = f"FACT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # Calcular totales
            subtotal = sum(detalle.total_linea for detalle in self.app.detalles_temp)
            
            # Calcular descuentos
            descuento = 0
            config = self.app.get_config()
            if (self.metodo_pago.get() == "EFECTIVO" and 
                config['habilitar_descuento_efectivo']):
                descuento += subtotal * (config['descuento_efectivo'] / 100)
            
            if self.app.cupon_aplicado:
                descuento += subtotal * (self.app.cupon_aplicado['descuento'] / 100)
            
            # Calcular base imponible
            base_imponible = subtotal - descuento
            
            # Calcular IVA
            iva = base_imponible * (config['porcentaje_iva'] / 100)
            total = base_imponible + iva
            
            # Insertar factura (con método de pago y descuento)
            self.app.get_db().execute_query(
                "INSERT INTO facturas (numero_factura, fecha, cliente_id, subtotal, descuento, iva, total, metodo_pago) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (numero_factura, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cliente_id, subtotal, descuento, iva, total, self.metodo_pago.get())
            )
            
            # Obtener ID de la factura insertada
            factura_id_result = self.app.get_db().fetch_one("SELECT last_insert_rowid()")
            if not factura_id_result:
                raise Exception("No se pudo obtener el ID de la factura insertada")
            
            factura_id = factura_id_result[0]
            
            # Insertar detalles
            for detalle in self.app.detalles_temp:
                # Buscar producto por código como texto
                producto_db = self.app.get_db().fetch_one("SELECT id FROM productos WHERE codigo = ?", (str(detalle.producto.codigo),))
                
                if not producto_db:
                    # Intentar buscar por nombre si no se encuentra por código
                    producto_db = self.app.get_db().fetch_one("SELECT id FROM productos WHERE nombre = ?", (detalle.producto.nombre,))
                    
                if not producto_db:
                    raise Exception(f"Producto '{detalle.producto.nombre}' (código: {detalle.producto.codigo}) no encontrado en la base de datos")
                
                producto_id = producto_db[0]
                
                self.app.get_db().execute_query(
                    "INSERT INTO detalles_factura (factura_id, producto_id, cantidad, precio_unitario, total_linea) VALUES (?, ?, ?, ?, ?)",
                    (factura_id, producto_id, detalle.cantidad, detalle.precio_unitario, detalle.total_linea)
                )
                
                # Actualizar stock (disminuir)
                self.app.get_db().execute_query(
                    "UPDATE productos SET stock = stock - ? WHERE id = ?",
                    (detalle.cantidad, producto_id)
                )
            
            # Actualizar uso de cupón si se aplicó
            if self.app.cupon_aplicado:
                self.app.get_db().execute_query(
                    "UPDATE cupones SET usos_actuales = usos_actuales + 1 WHERE id = ?",
                    (self.app.cupon_aplicado['id'],)
                )

            # Generar PDF
            from models import Factura
            factura_obj = Factura(
                id=factura_id,
                numero_factura=numero_factura,
                fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                cliente=cliente_obj,
                detalles=self.app.detalles_temp,
                subtotal=subtotal,
                descuento=descuento,
                iva=iva,
                total=total,
                metodo_pago=self.metodo_pago.get()
            )
            
            pdf_path = self.app.get_invoice_gen().generate_invoice(factura_obj)
            
            messagebox.showinfo("Éxito", f"Factura generada exitosamente\nGuardada en: {pdf_path}")
            self.limpiar_factura()
            self.app.productos_view.load_productos()  # Actualizar stock en la interfaz
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar factura: {str(e)}")
            import traceback
            print(traceback.format_exc())

    def limpiar_factura(self):
        self.app.detalles_temp = []
        for item in self.detalles_tree.get_children():
            self.detalles_tree.delete(item)
        self.calcular_totales()
        self.cliente_combobox.set('')
        self.metodo_pago.set("EFECTIVO")
        self.app.cupon_aplicado = None
        
        # Limpiar cliente manual si existe
        if hasattr(self.app, 'cliente_manual'):
            self.app.cliente_manual = None
        
        if hasattr(self, 'cupon_entry'):
            self.cupon_entry.delete(0, tk.END)
        if hasattr(self, 'cupon_status'):
            self.cupon_status.config(text="")