# models/cupon.py
from dataclasses import dataclass

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