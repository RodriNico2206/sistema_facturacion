import pywhatkit
import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from datetime import datetime, timedelta
import threading
import time

class WhatsAppSenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enviador de WhatsApp")
        self.root.geometry("500x550")
        self.root.configure(bg="#f0f8ff")
        
        # Inicializar sin archivo seleccionado
        self.archivo_path = ""
        self.numero_destino = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="Enviar Mensaje por WhatsApp", 
                              font=("Arial", 16, "bold"), bg="#25D366", fg="white")
        title_label.pack(fill="x", pady=10)
        
        # Marco principal
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Número de destino (EDITABLE)
        num_frame = tk.Frame(main_frame, bg="#f0f8ff")
        num_frame.pack(fill="x", pady=10)
        
        tk.Label(num_frame, text="Número de destino:", font=("Arial", 11, "bold"), 
                bg="#f0f8ff").pack(anchor="w")
        
        # Campo editable para el número
        self.num_entry = tk.Entry(num_frame, width=40, font=("Arial", 10))
        self.num_entry.pack(fill="x", pady=5)
        self.num_entry.insert(0, self.numero_destino)
        
        # Información del archivo
        file_frame = tk.Frame(main_frame, bg="#f0f8ff")
        file_frame.pack(fill="x", pady=10)
        
        tk.Label(file_frame, text="Archivo a enviar:", font=("Arial", 11, "bold"), 
                bg="#f0f8ff").pack(anchor="w")
        
        # Frame para botón y ruta de archivo
        file_selection_frame = tk.Frame(file_frame, bg="#f0f8ff")
        file_selection_frame.pack(fill="x", pady=5)
        
        # Botón para seleccionar archivo
        select_btn = tk.Button(file_selection_frame, text="Seleccionar Archivo", 
                              command=self.seleccionar_archivo, bg="#4FC3F7", fg="white",
                              font=("Arial", 10))
        select_btn.pack(side="left", padx=(0, 10))
        
        # Área para mostrar la ruta del archivo seleccionado
        self.file_text = tk.Text(file_selection_frame, height=2, width=30, font=("Arial", 9))
        self.file_text.pack(side="left", fill="x", expand=True)
        self.file_text.insert("1.0", "Ningún archivo seleccionado")
        self.file_text.config(state="disabled")
        
        # Estado del archivo
        self.status_label = tk.Label(file_frame, text="Seleccione un archivo", fg="gray", 
                                   font=("Arial", 10), bg="#f0f8ff")
        self.status_label.pack(anchor="w")
        
        # Mensaje (EDITABLE)
        msg_frame = tk.Frame(main_frame, bg="#f0f8ff")
        msg_frame.pack(fill="x", pady=10)
        
        tk.Label(msg_frame, text="Mensaje:", font=("Arial", 11, "bold"), 
                bg="#f0f8ff").pack(anchor="w")
        
        self.msg_text = tk.Text(msg_frame, height=3, width=40, font=("Arial", 10))
        self.msg_text.pack(fill="x", pady=5)
        self.msg_text.insert("1.0", "")
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg="#f0f8ff")
        btn_frame.pack(fill="x", pady=15)
        
        self.send_btn = tk.Button(btn_frame, text="Enviar Mensaje", command=self.enviar_mensaje,
                                 bg="#25D366", fg="white", font=("Arial", 12, "bold"))
        self.send_btn.pack(fill="x")
        
        # Barra de progreso
        self.progress = ttk.Progressbar(btn_frame, mode='indeterminate')
        self.progress.pack(fill="x", pady=5)
        
        # Estado
        self.status_var = tk.StringVar(value="Listo para enviar")
        status_label = tk.Label(btn_frame, textvariable=self.status_var, 
                               font=("Arial", 10), bg="#f0f8ff", fg="#555555")
        status_label.pack(anchor="w")
        
        # Información
        info_text = (
            "Notas importantes:\n"
            "1. Debes tener WhatsApp Web abierto en tu navegador\n"
            "2. La primera vez necesitarás escanear el código QR\n"
            "3. Asegúrate de que el archivo existe en la ruta especificada\n"
            "4. Formato número: +CódigoPaísNúmero (ej: +5491123456789)"
        )
        
        info_label = tk.Label(main_frame, text=info_text, justify="left",
                             font=("Arial", 9), bg="#f0f8ff", fg="#666666")
        info_label.pack(anchor="w", pady=(10, 0))
    
    def seleccionar_archivo(self):
        # Abrir diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo para enviar",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp"), 
                      ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.archivo_path = file_path
            self.file_text.config(state="normal")
            self.file_text.delete("1.0", "end")
            self.file_text.insert("1.0", self.archivo_path)
            self.file_text.config(state="disabled")
            
            # Verificar si el archivo existe
            archivo_existe = os.path.exists(self.archivo_path)
            status_text = "✓ Archivo encontrado" if archivo_existe else "✗ Archivo NO encontrado"
            status_color = "green" if archivo_existe else "red"
            
            self.status_label.config(text=status_text, fg=status_color)
    
    def enviar_mensaje(self):
        if not self.archivo_path:
            messagebox.showerror("Error", "Por favor, seleccione un archivo para enviar")
            return
            
        if not os.path.exists(self.archivo_path):
            messagebox.showerror("Error", f"El archivo no existe en:\n{self.archivo_path}")
            return
        
        # Obtener el número de destino
        self.numero_destino = self.num_entry.get().strip()
        if not self.numero_destino:
            messagebox.showerror("Error", "Por favor, ingrese un número de destino")
            return
        
        # Obtener el mensaje
        mensaje = self.msg_text.get("1.0", "end-1c").strip()
        
        # Deshabilitar botón y mostrar progreso
        self.send_btn.config(state="disabled")
        self.progress.start()
        self.status_var.set("Enviando mensaje...")
        
        # Ejecutar en un hilo separado
        thread = threading.Thread(target=self.enviar_mensaje_thread, args=(mensaje,))
        thread.daemon = True
        thread.start()
    
    def enviar_mensaje_thread(self, mensaje):
        try:
            # Calcular tiempo de envío (2 minutos desde ahora)
            ahora = datetime.now()
            tiempo_envio = ahora + timedelta(minutes=2)
            
            # Enviar la imagen
            pywhatkit.sendwhats_image(
                receiver=self.numero_destino,
                img_path=self.archivo_path,
                caption=mensaje,
                wait_time=50,
                tab_close=False
            )
            
            # Actualizar interfaz
            self.root.after(0, lambda: self.status_var.set("¡Mensaje enviado exitosamente!"))
            self.root.after(0, lambda: messagebox.showinfo("Éxito", "¡Mensaje enviado correctamente!"))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.status_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", f"No se pudo enviar el mensaje:\n{str(e)}"))
        
        finally:
            # Restaurar interfaz
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.send_btn.config(state="normal"))

# Función para uso programático (sin interfaz gráfica)
def enviar_whatsapp_programatico(numero_destino, archivo_path, mensaje=""):
    """
    Envía un mensaje de WhatsApp con imagen de forma programática
    
    Args:
        numero_destino (str): Número de destino con formato internacional
        archivo_path (str): Ruta completa al archivo de imagen
        mensaje (str): Mensaje opcional para enviar con la imagen
    
    Returns:
        bool: True si el envío fue exitoso, False si hubo error
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(archivo_path):
            print(f"Error: El archivo {archivo_path} no existe")
            return False
        
        # Verificar que se haya proporcionado un número
        if not numero_destino:
            print("Error: Debe proporcionar un número de destino")
            return False
        
        # Enviar la imagen
        pywhatkit.sendwhats_image(
            receiver=numero_destino,
            img_path=archivo_path,
            caption=mensaje,
            wait_time=50,
            tab_close=False
        )
        
        print("✅ Mensaje enviado exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error al enviar el mensaje: {str(e)}")
        return False

# Función para ejecutar la interfaz gráfica
def ejecutar_interfaz_whatsapp():
    """Ejecuta la interfaz gráfica del enviador de WhatsApp"""
    root = tk.Tk()
    app = WhatsAppSenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_interfaz_whatsapp()