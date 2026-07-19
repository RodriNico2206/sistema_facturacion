# Invoicing System
The Invoicing System is a comprehensive application designed to manage invoices, clients, products, and coupons. It provides a user-friendly interface for users to log in, view client information, manage products, and generate invoices.

## Key Features
* User authentication and authorization
* Client management
* Product management
* Coupon management
* Invoice generation
* Excel and PDF export

## Directory Hierarchy
```markdown
├── .gitignore
├── README.md
├── app.py
├── database.py
├── dialogs
│   ├── __init__.py
│   ├── cliente_dialog.py
│   ├── cliente_manual_dialog.py
│   ├── cupon_dialog.py
│   ├── producto_dialog.py
├── estructura_propuesta.txt
├── login_window.py
├── main.py
├── models
│   ├── __init__.py
│   ├── cliente.py
│   ├── configuracion.py
│   ├── cupon.py
│   ├── detalle_factura.py
│   ├── factura.py
│   ├── producto.py
├── models.py
├── templates
│   ├── invoice_template.html
├── utils
│   ├── __init__.py
│   ├── config_manager.py
│   ├── excel_utils.py
│   ├── invoice_generator.py
│   ├── pdf_converter_module.py
│   ├── whatsapp_sender_module.py
├── views
    ├── __init__.py
    ├── clientes_view.py
    ├── configuracion_view.py
    ├── cupones_view.py
    ├── facturacion_view.py
    ├── facturas_view.py
    ├── productos_view.py
    ├── usuarios_view.py
```

## Module Functionality
The Invoicing System consists of several modules that interact with each other to provide a comprehensive invoicing solution. The `main.py` file serves as the entry point of the application, responsible for initializing the database, displaying the login window, and starting the main application. The `database.py` file handles database operations, while the `models` folder contains classes that represent the data structures used in the application. The `dialogs` folder contains classes that handle user interactions, such as client and product management. The `utils` folder contains utility classes that provide additional functionality, such as invoice generation and PDF conversion.

## Prerequisites and Installation
To run the Invoicing System, you will need to have Python and the required libraries installed. The application uses the following libraries:
* `tkinter` for the graphical user interface
* `database` for database operations

## Usage Example
```python
if __name__ == "__main__":
    sistema = SistemaFacturacion()
    sistema.run()
```

## Usage Restrictions
The Invoicing System is designed to run on a local machine and requires a database to be set up. The application may not work properly if the database is not configured correctly.

## Workflow Diagram
```mermaid
graph LR
    A[User] -->|Login|> B[Login Window]
    B -->|Authenticate|> C[Database]
    C -->|Authorize|> D[Main Application]
    D -->|Manage Clients|> E[Client Management]
    D -->|Manage Products|> F[Product Management]
    D -->|Generate Invoice|> G[Invoice Generation]
    G -->|Export to Excel|> H[Excel Export]
    G -->|Export to PDF|> I[PDF Export]
```