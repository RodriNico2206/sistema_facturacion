# models/__init__.py
from .cliente import Cliente
from .producto import Producto
from .factura import Factura
from .detalle_factura import DetalleFactura
from .configuracion import Configuracion
from .cupon import Cupon

__all__ = ['Cliente', 'Producto', 'Factura', 'DetalleFactura', 'Configuracion', 'Cupon']