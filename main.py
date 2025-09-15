# main.py
import tkinter as tk
from database import Database
from login_window import LoginWindow
from app import FacturacionApp

class SistemaFacturacion:
    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.mostrar_login()
    
    def mostrar_login(self):
        """Muestra la pantalla de login"""
        login_root = tk.Toplevel(self.root)
        login_root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
        
        LoginWindow(login_root, self.db, self.iniciar_aplicacion_principal)
    
    def iniciar_aplicacion_principal(self):
        """Inicia la aplicación principal después del login exitoso"""
        self.root.deiconify()  # Muestra la ventana principal
        self.app = FacturacionApp(self.root)
    
    def cerrar_aplicacion(self):
        """Cierra completamente la aplicación"""
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.withdraw()  # Oculta la ventana principal inicialmente
        self.root.mainloop()

if __name__ == "__main__":
    sistema = SistemaFacturacion()
    sistema.run()