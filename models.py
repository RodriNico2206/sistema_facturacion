from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Cliente:
    id: int = None
    nombre: str = ""
    dni: str = ""  # Cambiado de ruc a dni
    direccion: str = ""
    telefono: str = ""
    email: str = ""

@dataclass
class Producto:
    id: int = None
    codigo: str = ""
    nombre: str = ""
    descripcion: str = ""
    precio: float = 0.0
    stock: int = 0

@dataclass
class DetalleFactura:
    producto: Producto
    cantidad: int
    precio_unitario: float
    total_linea: float

@dataclass
class Configuracion:
    porcentaje_iva: float = 12.0
    descuento_efectivo: float = 5.0
    habilitar_descuento_efectivo: bool = True
    habilitar_cupones: bool = False

@dataclass
class Cupon:
    id: int = None
    codigo: str = ""
    descuento: float = 0.0
    valido_desde: str = ""
    valido_hasta: str = ""
    usos_maximos: int = 1
    usos_actuales: int = 0
    activo: bool = True

@dataclass
class Factura:
    id: int = None
    numero_factura: str = ""
    fecha: str = ""
    cliente: Cliente = None
    detalles: List[DetalleFactura] = None
    subtotal: float = 0.0
    descuento: float = 0.0  # Nuevo campo para descuentos
    iva: float = 0.0
    total: float = 0.0
    metodo_pago: str = "EFECTIVO"  # Nuevo campo para método de pago
    estado: str = "PENDIENTE"
    
    def __post_init__(self):
        if self.detalles is None:
            self.detalles = []
        if not self.fecha:
            self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")