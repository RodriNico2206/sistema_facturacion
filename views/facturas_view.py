# views/facturas_view.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading
from datetime import datetime
from utils.pdf_converter_module import convertir_pdf_programatico
from utils.whatsapp_sender_module import enviar_whatsapp_programatico


class FacturasView:
    def __init__(self, parent, app):
        self.app = app
        self.frame = ttk.Frame(parent)
        self.factura_seleccionada = None
        self.setup_ui()
        
    def setup_ui(self):
        # Treeview para facturas
        columns = ('id', 'numero_factura', 'fecha', 'cliente', 'total', 'archivo')
        self.facturas_tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.facturas_tree.heading('id', text='ID')
        self.facturas_tree.heading('numero_factura', text='Número Factura')
        self.facturas_tree.heading('fecha', text='Fecha')
        self.facturas_tree.heading('cliente', text='Cliente')
        self.facturas_tree.heading('total', text='Total')
        self.facturas_tree.heading('archivo', text='Archivo PDF')
        
        self.facturas_tree.column('id', width=50)
        self.facturas_tree.column('numero_factura', width=120)
        self.facturas_tree.column('fecha', width=120)
        self.facturas_tree.column('cliente', width=150)
        self.facturas_tree.column('total', width=80)
        self.facturas_tree.column('archivo', width=200)
        
        self.facturas_tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.facturas_tree.bind('<<TreeviewSelect>>', self.on_factura_seleccionada)
        
        # Frame para botones
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)
        
        # Botón para cargar facturas
        ttk.Button(button_frame, text="Actualizar Lista", command=self.load_facturas).pack(side='left', padx=5)
        
        # Botón para abrir factura
        self.abrir_btn = ttk.Button(button_frame, text="Abrir Factura", 
                                   command=self.abrir_factura, state='disabled')
        self.abrir_btn.pack(side='left', padx=5)
        
        # Botón para convertir a imagen
        self.convertir_btn = ttk.Button(button_frame, text="Convertir a Imagen", 
                                       command=self.convertir_a_imagen, state='disabled')
        self.convertir_btn.pack(side='left', padx=5)
        
        # Botón para enviar por WhatsApp
        self.whatsapp_btn = ttk.Button(button_frame, text="Enviar por WhatsApp", 
                                      command=self.enviar_whatsapp, state='disabled')
        self.whatsapp_btn.pack(side='left', padx=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(button_frame, mode='indeterminate')
        self.progress.pack(side='left', padx=5, fill='x', expand=True)
        
        # Estado
        self.status_var = tk.StringVar(value="Listo")
        status_label = ttk.Label(button_frame, textvariable=self.status_var)
        status_label.pack(side='left', padx=5)
        
        # Cargar facturas
        self.load_facturas()
    
    def load_facturas(self):
        """Carga las facturas desde la base de datos"""
        facturas = self.app.get_db().fetch_all("""
            SELECT f.id, f.numero_factura, f.fecha, c.nombre, f.total 
            FROM facturas f 
            LEFT JOIN clientes c ON f.cliente_id = c.id 
            ORDER BY f.fecha DESC
        """)
        
        # Limpiar treeview
        for item in self.facturas_tree.get_children():
            self.facturas_tree.delete(item)
        
        # Insertar facturas
        for factura in facturas:
            # Construir nombre de archivo
            archivo_pdf = f"facturas/factura_{factura[1]}.pdf"
            archivo_existe = "Sí" if os.path.exists(archivo_pdf) else "No"
            
            self.facturas_tree.insert('', 'end', values=(
                factura[0],  # id
                factura[1],  # numero_factura
                factura[2],  # fecha
                factura[3],  # cliente
                f"${factura[4]:.2f}",  # total
                archivo_existe  # archivo
            ))
    
    def on_factura_seleccionada(self, event):
        """Maneja la selección de una factura"""
        selection = self.facturas_tree.selection()
        if selection:
            item = self.facturas_tree.item(selection[0])
            self.factura_seleccionada = item['values']
            
            # Habilitar botones si el archivo existe
            archivo_existe = item['values'][5] == "Sí"
            self.abrir_btn.config(state='normal' if archivo_existe else 'disabled')
            self.convertir_btn.config(state='normal')
            self.whatsapp_btn.config(state='normal' if archivo_existe else 'disabled')
        else:
            self.factura_seleccionada = None
            self.abrir_btn.config(state='disabled')
            self.convertir_btn.config(state='disabled')
            self.whatsapp_btn.config(state='disabled')
    
    def abrir_factura(self):
        """Abre la factura PDF con el programa predeterminado"""
        if not self.factura_seleccionada:
            return
            
        numero_factura = self.factura_seleccionada[1]
        pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "facturas", f"factura_{numero_factura}.pdf")
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(pdf_path)
            elif os.name == 'posix':  # macOS, Linux
                import subprocess
                opener = 'open' if os.uname().sysname == 'Darwin' else 'xdg-open'
                subprocess.call([opener, pdf_path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")
    
    def convertir_a_imagen(self):
        """Convierte la factura PDF a imagen JPG"""
        if not self.factura_seleccionada:
            return
            
        numero_factura = self.factura_seleccionada[1]
        pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "facturas", f"factura_{numero_factura}.pdf")
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", "El archivo PDF no existe")
            return
        
        # Deshabilitar botones y mostrar progreso
        self.set_ui_state(False)
        self.progress.start()
        self.status_var.set("Convirtiendo a imagen...")
        
        # Ejecutar en un hilo separado
        thread = threading.Thread(target=self.convertir_thread, args=(pdf_path,))
        thread.daemon = True
        thread.start()
    
    def convertir_thread(self, pdf_path):
        """Hilo para convertir PDF a imagen"""
        try:
            
            # Crear carpeta para imágenes si no existe
            output_folder = "facturas_imagenes"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Convertir PDF a JPG
            success = convertir_pdf_programatico(pdf_path, output_folder, dpi=300)
            
            if success:
                self.app.after(0, lambda: self.status_var.set("✅ Conversión completada"))
                self.app.after(0, lambda: messagebox.showinfo("Éxito", "Factura convertida a imagen correctamente"))
            else:
                self.app.after(0, lambda: self.status_var.set("❌ Error en conversión"))
                self.app.after(0, lambda: messagebox.showerror("Error", "No se pudo convertir la factura"))
                
        except Exception as e:
            self.app.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.app.after(0, lambda: messagebox.showerror("Error", f"No se pudo convertir: {str(e)}"))
        
        finally:
            # Restaurar interfaz
            self.app.after(0, lambda: self.progress.stop())
            self.app.after(0, lambda: self.set_ui_state(True))
    
    def enviar_whatsapp(self):
        """Envía la factura por WhatsApp"""
        if not self.factura_seleccionada:
            return
            
        numero_factura = self.factura_seleccionada[1]
        pdf_path = f"facturas/factura_{numero_factura}.pdf"
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", "El archivo PDF no existe")
            return
        
        # Pedir número de destino
        numero_destino = self.pedir_numero_destino()
        if not numero_destino:
            return
        
        # Deshabilitar botones y mostrar progreso
        self.set_ui_state(False)
        self.progress.start()
        self.status_var.set("Enviando por WhatsApp...")
        
        # Ejecutar en un hilo separado
        thread = threading.Thread(target=self.enviar_whatsapp_thread, 
                                args=(pdf_path, numero_destino))
        thread.daemon = True
        thread.start()
    
    def pedir_numero_destino(self):
        """Dialogo para pedir número de destino"""
        dialog = tk.Toplevel(self.frame)
        dialog.title("Número de WhatsApp")
        dialog.geometry("400x150")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Ingrese el número de WhatsApp (con código de país):").pack(pady=10)
        
        numero_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=numero_var, width=30)
        entry.pack(pady=5)
        entry.focus()
        
        resultado = [None]  # Usar lista para pasar por referencia
        
        def on_ok():
            resultado[0] = numero_var.get().strip()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="OK", command=on_ok).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancelar", command=on_cancel).pack(side='left', padx=5)
        
        self.frame.wait_window(dialog)
        return resultado[0]
    
    def enviar_whatsapp_thread(self, pdf_path, numero_destino):
        """Hilo para enviar por WhatsApp"""
        try:
            
            output_folder = "temp_whatsapp"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            
            # Convertir PDF a JPG
            success = convertir_pdf_programatico(pdf_path, output_folder, dpi=150)
            
            if not success:
                self.app.after(0, lambda: self.status_var.set("❌ Error en conversión"))
                self.app.after(0, lambda: messagebox.showerror("Error", "No se pudo convertir la factura para WhatsApp"))
                return
            
            # Buscar el archivo JPG convertido
            jpg_files = [f for f in os.listdir(output_folder) if f.endswith('.jpg')]
            if not jpg_files:
                self.app.after(0, lambda: self.status_var.set("❌ No se encontró imagen"))
                return
            
            jpg_path = os.path.join(output_folder, jpg_files[0])
            
            
            # Crear mensaje con información de la factura
            mensaje = f"Factura {self.factura_seleccionada[1]}\nCliente: {self.factura_seleccionada[3]}\nTotal: {self.factura_seleccionada[4]}"
            
            success = enviar_whatsapp_programatico(numero_destino, jpg_path, mensaje)
            
            if success:
                self.app.after(0, lambda: self.status_var.set("✅ Enviado por WhatsApp"))
                self.app.after(0, lambda: messagebox.showinfo("Éxito", "Factura enviada por WhatsApp correctamente"))
            else:
                self.app.after(0, lambda: self.status_var.set("❌ Error al enviar"))
                self.app.after(0, lambda: messagebox.showerror("Error", "No se pudo enviar por WhatsApp"))
                
        except Exception as e:
            self.app.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            self.app.after(0, lambda: messagebox.showerror("Error", f"No se pudo enviar: {str(e)}"))
        
        finally:
            # Limpiar archivos temporales
            try:
                import shutil
                if os.path.exists(output_folder):
                    shutil.rmtree(output_folder)
            except:
                pass
            
            # Restaurar interfaz
            self.app.after(0, lambda: self.progress.stop())
            self.app.after(0, lambda: self.set_ui_state(True))
    
    # def set_ui_state(self, enabled):
    #     """Habilita o deshabilita los controles de UI"""
    #     state = 'normal' if enabled else 'disabled'
    #     self.abrir_btn.config(state=state)
    #     self.convertir_btn.config(state=state)
    #     self.whatsapp_btn.config(state=state)
        
    #     # También habilitar/deshabilitar la selección en el treeview
    #     for btn in self.frame.winfo_children()[1].winfo_children():  # Botones
    #         if hasattr(btn, 'config') and btn not in [self.abrir_btn, self.convertir_btn, self.whatsapp_btn]:
    #             btn.config(state=state)
    def set_ui_state(self, enabled):
        """Habilita o deshabilita los controles de UI"""
        state = 'normal' if enabled else 'disabled'
        
        # Botones principales
        self.abrir_btn.config(state=state)
        self.convertir_btn.config(state=state)
        self.whatsapp_btn.config(state=state)
        
        # Filtrar solo widgets que son botones y tienen la opción state
        for widget in self.frame.winfo_children()[1].winfo_children():
            if isinstance(widget, tk.Button) or (hasattr(widget, 'config') and 'state' in widget.keys()):
                try:
                    widget.config(state=state)
                except:
                    # Si falla, continuar con el siguiente widget
                    continue