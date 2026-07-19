# Invoicing System
The Invoicing System is a comprehensive application designed to manage invoices, clients, products, and coupons. It provides a user-friendly interface for users to log in, view client information, manage products, and generate invoices.

## Key Features
* User authentication and authorization
* Client management
* Product management
* Coupon management
* Invoice generation
* Integration with WhatsApp for sending invoices

## Directory Hierarchy
```markdown
.
├── .gitignore
├── README.md
├── app.py
├── database.py
├── dialogs
│   ├── __init__.py
│   ├── cliente_dialog.py
│   ├── cliente_manual_dialog.py
│   ├── cupon_dialog.py
│   └── producto_dialog.py
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
│   └── producto.py
├── models.py
├── templates
│   └── invoice_template.html
├── utils
│   ├── __init__.py
│   ├── config_manager.py
│   ├── excel_utils.py
│   ├── invoice_generator.py
│   ├── pdf_converter_module.py
│   └── whatsapp_sender_module.py
└── views
    ├── __init__.py
    ├── clientes_view.py
    ├── configuracion_view.py
    ├── cupones_view.py
    ├── facturacion_view.py
    ├── facturas_view.py
    ├── productos_view.py
    └── usuarios_view.py
```

## Module Functionality
The Invoicing System consists of several modules that interact with each other to provide the core functionality. The `database.py` module handles database operations, while the `models` module defines the data structures for clients, products, coupons, and invoices. The `dialogs` module contains the UI components for interacting with clients, products, and coupons. The `utils` module provides utility functions for generating invoices, converting to PDF, and sending via WhatsApp. The `views` module defines the UI components for the main application.

## Prerequisites and Installation
To run the Invoicing System, you need to have Python 3.x installed, along with the required libraries:
* `tkinter` for the UI
* `database` for database operations

## Usage Example
```python
if __name__ == "__main__":
    sistema = SistemaFacturacion()
    sistema.run()
```

## Usage Restrictions
The Invoicing System requires a valid database connection to function properly. Additionally, the WhatsApp integration requires a valid WhatsApp account and phone number.

## Workflow Diagram
```mermaid
A[User] -->|Login| B[Login Window]
B -->|Valid Credentials| C[Main Application]
C -->|Client Management| D[Client Dialog]
C -->|Product Management| E[Product Dialog]
C -->|Coupon Management| F[Coupon Dialog]
C -->|Invoice Generation| G[Invoice Generator]
G -->|PDF Conversion| H[PDF Converter]
H -->|WhatsApp Sending| I[WhatsApp Sender]
```