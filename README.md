# Sistema de Facturación
Sistema de Facturación es una aplicación de escritorio diseñada para gestionar facturas y usuarios. La aplicación cuenta con una interfaz gráfica de usuario intuitiva y fácil de usar, lo que la hace ideal para pequeñas y medianas empresas.

## Características clave
* Interfaz gráfica de usuario intuitiva
* Gestión de usuarios y sesiones
* Funcionalidad de facturación completa
* Conexión a base de datos para almacenar información
* Cierre seguro de la aplicación

## Requisitos previos e instalación
Para ejecutar la aplicación, se requieren los siguientes componentes:
* Python 3.x
* Biblioteca `tkinter` para la interfaz gráfica de usuario
* Biblioteca `database` para la conexión a la base de datos (no incluida en el código proporcionado)
* Módulos `login_window` y `app` (incluidos en el código proporcionado)

## Ejemplo de uso
```python
# Crear una instancia de la clase SistemaFacturacion
sistema = SistemaFacturacion()

# Ejecutar la aplicación
sistema.run()
```
Este ejemplo muestra cómo crear una instancia de la clase `SistemaFacturacion` y ejecutar la aplicación. La aplicación se iniciará mostrando la pantalla de login, donde el usuario podrá ingresar sus credenciales para acceder a la aplicación principal.