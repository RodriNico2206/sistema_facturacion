import sqlite3, hashlib
from datetime import datetime

class Database:
    def __init__(self, db_name="facturacion.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nombre TEXT NOT NULL,
                email TEXT,
                activo INTEGER DEFAULT 1,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Resto de las tablas existentes (clientes, productos, etc.)
        # ... (el resto de tu código existente)
        
        # Tabla de clientes (cambiamos RUC por DNI)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dni TEXT,
                direccion TEXT,
                telefono TEXT,
                email TEXT
            )
        ''')
        
        # Tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                stock INTEGER DEFAULT 0
            )
        ''')
        
        # Tabla de facturas (agregamos campo de método de pago)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE NOT NULL,
                fecha TEXT NOT NULL,
                cliente_id INTEGER,
                subtotal REAL,
                descuento REAL DEFAULT 0,
                iva REAL,
                total REAL,
                metodo_pago TEXT DEFAULT 'EFECTIVO',
                estado TEXT DEFAULT 'PENDIENTE',
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')
        
        # Tabla de detalles de factura
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalles_factura (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER,
                precio_unitario REAL,
                total_linea REAL,
                FOREIGN KEY (factura_id) REFERENCES facturas (id),
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        ''')
        
        # Tabla de configuración
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                porcentaje_iva REAL DEFAULT 12.0,
                descuento_efectivo REAL DEFAULT 5.0,
                habilitar_descuento_efectivo INTEGER DEFAULT 1,
                habilitar_cupones INTEGER DEFAULT 0
            )
        ''')
        
        # Tabla de cupones de descuento
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cupones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                descuento REAL NOT NULL,
                valido_desde TEXT,
                valido_hasta TEXT,
                usos_maximos INTEGER DEFAULT 1,
                usos_actuales INTEGER DEFAULT 0,
                activo INTEGER DEFAULT 1
            )
        ''')
        
        # Insertar configuración por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM configuracion")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO configuracion (porcentaje_iva, descuento_efectivo) VALUES (?, ?)",
                (12.0, 5.0)
            )

        # Insertar usuario admin por defecto si no existe
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            password_hash = self.hash_password("admin123")
            cursor.execute(
                "INSERT INTO usuarios (username, password, nombre, email) VALUES (?, ?, ?, ?)",
                ("admin", password_hash, "Administrador", "admin@empresa.com")
            )
        
        self.conn.commit()

    def hash_password(self, password):
        """Encripta la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_usuario(self, username, password):
        """Verifica las credenciales del usuario"""
        cursor = self.conn.cursor()
        password_hash = self.hash_password(password)
        
        cursor.execute(
            "SELECT id, username, nombre FROM usuarios WHERE username = ? AND password = ? AND activo = 1",
            (username, password_hash)
        )
        
        return cursor.fetchone()


    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor
    
    def fetch_all(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()