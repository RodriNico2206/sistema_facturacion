# models/factura.py
from dataclasses import dataclass
from typing import List
from datetime import datetime
from .cliente import Cliente
from .detalle_factura import DetalleFactura

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