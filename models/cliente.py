# models/cliente.py
from dataclasses import dataclass

@dataclass
class Cliente:
    id: int = None
    nombre: str = ""
    dni: str = ""  # Cambiado de ruc a dni
    direccion: str = ""
    telefono: str = ""
    email: str = ""