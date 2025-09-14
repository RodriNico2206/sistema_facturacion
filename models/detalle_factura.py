# models/detalle_factura.py
from dataclasses import dataclass
from .producto import Producto

@dataclass
class DetalleFactura:
    producto: Producto
    cantidad: int
    precio_unitario: float
    total_linea: float