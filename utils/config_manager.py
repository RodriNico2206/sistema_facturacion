# utils/config_manager.py
class ConfigManager:
    def __init__(self, db):
        self.db = db
        
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
        
    def guardar_configuracion(self, configuracion):
        """Guarda la configuración en la base de datos"""
        self.db.execute_query("DELETE FROM configuracion")
        self.db.execute_query(
            "INSERT INTO configuracion (porcentaje_iva, descuento_efectivo, habilitar_descuento_efectivo, habilitar_cupones) VALUES (?, ?, ?, ?)",
            (configuracion['porcentaje_iva'], configuracion['descuento_efectivo'], 
             int(configuracion['habilitar_descuento_efectivo']), int(configuracion['habilitar_cupones']))
        )