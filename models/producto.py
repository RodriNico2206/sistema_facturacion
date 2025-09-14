# models/producto.py
from dataclasses import dataclass

@dataclass
class Producto:
    id: int = None
    codigo: str = ""
    nombre: str = ""
    descripcion: str = ""
    precio: float = 0.0
    stock: int = 0