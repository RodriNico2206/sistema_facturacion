import fitz  # PyMuPDF
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class PDFtoJPGConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor PDF a JPG")
        self.root.geometry("500x300")
        self.root.configure(bg="#f0f8ff")
        
        self.pdf_path = ""
        self.output_folder = ""
        
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        title_label = tk.Label(self.root, text="Conversor PDF a JPG", 
                              font=("Arial", 16, "bold"), bg="#2E86C1", fg="white")
        title_label.pack(fill="x", pady=10)
        
        # Marco principal
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Selección de archivo PDF
        pdf_frame = tk.Frame(main_frame, bg="#f0f8ff")
        pdf_frame.pack(fill="x", pady=10)
        
        tk.Label(pdf_frame, text="Archivo PDF:", font=("Arial", 11, "bold"), 
                bg="#f0f8ff").pack(anchor="w")
        
        # Frame para botón y ruta de PDF
        pdf_selection_frame = tk.Frame(pdf_frame, bg="#f0f8ff")
        pdf_selection_frame.pack(fill="x", pady=5)
        
        # Botón para seleccionar PDF
        pdf_btn = tk.Button(pdf_selection_frame, text="Seleccionar PDF", 
                           command=self.seleccionar_pdf, bg="#3498DB", fg="white",
                           font=("Arial", 10))
        pdf_btn.pack(side="left", padx=(0, 10))
        
        # Área para mostrar la ruta del PDF seleccionado
        self.pdf_text = tk.Text(pdf_selection_frame, height=2, width=30, font=("Arial", 9))
        self.pdf_text.pack(side="left", fill="x", expand=True)
        self.pdf_text.insert("1.0", "Ningún PDF seleccionado")
        self.pdf_text.config(state="disabled")
        
        # Selección de carpeta destino
        folder_frame = tk.Frame(main_frame, bg="#f0f8ff")
        folder_frame.pack(fill="x", pady=10)
        
        tk.Label(folder_frame, text="Carpeta destino:", font=("Arial", 11, "bold"), 
                bg="#f0f8ff").pack(anchor="w")
        
        # Frame para botón y ruta de carpeta
        folder_selection_frame = tk.Frame(folder_frame, bg="#f0f8ff")
        folder_selection_frame.pack(fill="x", pady=5)
        
        # Botón para seleccionar carpeta
        folder_btn = tk.Button(folder_selection_frame, text="Seleccionar Carpeta", 
                              command=self.seleccionar_carpeta, bg="#3498DB", fg="white",
                              font=("Arial", 10))
        folder_btn.pack(side="left", padx=(0, 10))
        
        # Área para mostrar la ruta de la carpeta seleccionada
        self.folder_text = tk.Text(folder_selection_frame, height=2, width=30, font=("Arial", 9))
        self.folder_text.pack(side="left", fill="x", expand=True)
        self.folder_text.insert("1.0", "Ninguna carpeta seleccionada")
        self.folder_text.config(state="disabled")
        
        # Configuración de DPI
        dpi_frame = tk.Frame(main_frame, bg="#f0f8ff")
        dpi_frame.pack(fill="x", pady=10)
        
        tk.Label(dpi_frame, text="Calidad (DPI):", font=("Arial", 11, "bold"), 
                bg="#f0f8ff").pack(anchor="w")
        
        self.dpi_var = tk.IntVar(value=300)
        dpi_spinbox = tk.Spinbox(dpi_frame, from_=72, to=600, increment=50, 
                                textvariable=self.dpi_var, width=10, font=("Arial", 10))
        dpi_spinbox.pack(anchor="w", pady=5)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg="#f0f8ff")
        btn_frame.pack(fill="x", pady=15)
        
        self.convert_btn = tk.Button(btn_frame, text="Convertir a JPG", command=self.convertir_pdf,
                                    bg="#27AE60", fg="white", font=("Arial", 12, "bold"))
        self.convert_btn.pack(fill="x")
        
        # Barra de progreso
        self.progress = ttk.Progressbar(btn_frame, mode='indeterminate')
        self.progress.pack(fill="x", pady=5)
        
        # Estado
        self.status_var = tk.StringVar(value="Listo para convertir")
        status_label = tk.Label(btn_frame, textvariable=self.status_var, 
                               font=("Arial", 10), bg="#f0f8ff", fg="#555555")
        status_label.pack(anchor="w")
    
    def seleccionar_pdf(self):
        # Abrir diálogo para seleccionar archivo PDF
        pdf_path = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        
        if pdf_path:
            self.pdf_path = pdf_path
            self.pdf_text.config(state="normal")
            self.pdf_text.delete("1.0", "end")
            self.pdf_text.insert("1.0", self.pdf_path)
            self.pdf_text.config(state="disabled")
            self.actualizar_estado()
    
    def seleccionar_carpeta(self):
        # Abrir diálogo para seleccionar carpeta
        output_folder = filedialog.askdirectory(
            title="Seleccionar carpeta de destino"
        )
        
        if output_folder:
            self.output_folder = output_folder
            self.folder_text.config(state="normal")
            self.folder_text.delete("1.0", "end")
            self.folder_text.insert("1.0", self.output_folder)
            self.folder_text.config(state="disabled")
            self.actualizar_estado()
    
    def actualizar_estado(self):
        # Actualizar el estado según las selecciones
        if self.pdf_path and self.output_folder:
            self.status_var.set("Listo para convertir")
            self.convert_btn.config(state="normal")
        else:
            self.status_var.set("Seleccione archivo PDF y carpeta destino")
            self.convert_btn.config(state="disabled")
    
    def convertir_pdf(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Por favor, seleccione un archivo PDF")
            return
            
        if not self.output_folder:
            messagebox.showerror("Error", "Por favor, seleccione una carpeta destino")
            return
        
        # Deshabilitar botón y mostrar progreso
        self.convert_btn.config(state="disabled")
        self.progress.start()
        self.status_var.set("Convirtiendo PDF...")
        
        # Ejecutar en un hilo separado
        thread = threading.Thread(target=self.convertir_pdf_thread)
        thread.daemon = True
        thread.start()
    
    def convertir_pdf_thread(self):
        try:
            # Verificar si el archivo existe
            if not os.path.exists(self.pdf_path):
                self.root.after(0, lambda: messagebox.showerror("Error", f"El archivo no existe:\n{self.pdf_path}"))
                return
            
            # Crear carpeta de salida si no existe
            if not os.path.exists(self.output_folder):
                os.makedirs(self.output_folder)
            
            # Obtener el nombre base del archivo PDF (sin extensión)
            pdf_filename = os.path.basename(self.pdf_path)
            base_name = os.path.splitext(pdf_filename)[0]
            
            # Abrir el PDF
            doc = fitz.open(self.pdf_path)
            total_paginas = len(doc)
            
            # Calcular factor de zoom basado en DPI
            zoom = self.dpi_var.get() / 72
            matrix = fitz.Matrix(zoom, zoom)
            
            # Convertir cada página
            for page_num in range(total_paginas):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=matrix)
                
                # Guardar como JPG con el nombre base + número de página
                output_path = os.path.join(self.output_folder, f"{base_name}_pag{page_num + 1}.jpg")
                pix.save(output_path, "jpeg")
            
            # Cerrar el documento
            doc.close()
            
            # Crear mensaje personalizado según el número de páginas
            if total_paginas == 1:
                archivos_msg = f"{base_name}_pag1.jpg"
            elif total_paginas == 2:
                archivos_msg = f"{base_name}_pag1.jpg\n{base_name}_pag2.jpg"
            else:
                archivos_msg = f"{base_name}_pag1.jpg\n{base_name}_pag2.jpg\n...\n{base_name}_pag{total_paginas}.jpg"
            
            # Actualizar interfaz
            self.root.after(0, lambda: self.status_var.set(f"✅ Conversión completada! {total_paginas} páginas convertidas."))
            self.root.after(0, lambda: messagebox.showinfo("Éxito", f"Conversión completada! {total_paginas} página(s) convertida(s).\n\nArchivos guardados como:\n{archivos_msg}"))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.status_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", f"No se pudo convertir el PDF:\n{str(e)}"))
        
        finally:
            # Restaurar interfaz
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.convert_btn.config(state="normal"))

# Función para uso programático (sin interfaz gráfica)
def convertir_pdf_programatico(pdf_path, output_folder, dpi=300):
    """
    Convierte un PDF a imágenes JPG sin interfaz gráfica
    
    Args:
        pdf_path (str): Ruta completa al archivo PDF
        output_folder (str): Carpeta donde guardar las imágenes
        dpi (int): Resolución de las imágenes (por defecto 300)
    
    Returns:
        bool: True si la conversión fue exitosa, False si hubo error
    """
    try:
        # Verificar si el archivo existe
        if not os.path.exists(pdf_path):
            print(f"Error: El archivo {pdf_path} no existe")
            return False
        
        # Crear carpeta de salida si no existe
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Carpeta creada: {output_folder}")
        
        # Obtener el nombre base del archivo PDF (sin extensión)
        pdf_filename = os.path.basename(pdf_path)
        base_name = os.path.splitext(pdf_filename)[0]
        
        # Abrir el PDF
        doc = fitz.open(pdf_path)
        total_paginas = len(doc)
        
        # Calcular factor de zoom basado en DPI
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        
        # Convertir cada página
        for page_num in range(total_paginas):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=matrix)
            
            # Guardar como JPG con el nombre base + número de página
            output_path = os.path.join(output_folder, f"{base_name}_pag{page_num + 1}.jpg")
            pix.save(output_path, "jpeg")
            print(f"✓ Página {page_num + 1} guardada como {output_path}")
        
        # Cerrar el documento
        doc.close()
        
        print(f"✅ Conversión completada! {total_paginas} páginas convertidas.")
        return True
        
    except Exception as e:
        print(f"❌ Error al procesar el PDF: {str(e)}")
        return False

# Función para ejecutar la interfaz gráfica
def ejecutar_interfaz():
    """Ejecuta la interfaz gráfica del conversor"""
    root = tk.Tk()
    app = PDFtoJPGConverter(root)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_interfaz()