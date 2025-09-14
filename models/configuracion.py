# models/configuracion.py
from dataclasses import dataclass

@dataclass
class Configuracion:
    porcentaje_iva: float = 12.0
    descuento_efectivo: float = 5.0
    habilitar_descuento_efectivo: bool = True
    habilitar_cupones: bool = False