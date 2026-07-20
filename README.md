# Invoicing System
The Invoicing System is a comprehensive application designed to manage invoices, clients, products, and coupons for a business. It provides a user-friendly interface for users to log in, view, and manage their data.

## Key Features
* User authentication and authorization
* Client management
* Product management
* Coupon management
* Invoice generation
* Excel and PDF export

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
The Invoicing System consists of several modules, each responsible for a specific functionality:
* `app.py`: The main application module.
* `database.py`: Handles database operations.
* `dialogs`: Contains dialog windows for client, product, and coupon management.
* `models`: Defines data models for clients, products, coupons, and invoices.
* `utils`: Provides utility functions for invoice generation, Excel and PDF export, and WhatsApp sending.
* `views`: Contains view classes for client, product, coupon, and invoice management.

## Prerequisites and Environment Setup
To run the Invoicing System, you will need:
* Python 3.x
* Tkinter library
* A database (configured in `database.py`)
### Configuration
No environment variables or JSON configuration files are required for this project.

## Installation
To install the Invoicing System, follow these steps:
1. Create a virtual environment using `python -m venv venv`.
2. Activate the virtual environment using `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows).
3. Install the required dependencies using `pip install -r requirements.txt`.

## Usage Example
To run the Invoicing System, execute the following command:
```bash
python main.py
```

## Usage Restrictions
The Invoicing System requires a database to be configured in `database.py`. The system also uses Tkinter for the graphical user interface, which may have limitations on certain platforms.

## Workflow Diagram
```mermaid
graph LR
    A[User] -->|Login| B[Login Window]
    B -->|Authenticate| C[Database]
    C -->|Authorize| D[Main Application]
    D -->|Manage Data| E[Client/Product/Coupon Management]
    E -->|Generate Invoice| F[Invoice Generation]
    F -->|Export to Excel/PDF| G[Excel/PDF Export]
    G -->|Send via WhatsApp| H[WhatsApp Sending]
```
Note: This diagram illustrates the high-level workflow of the Invoicing System. The actual implementation may vary depending on the specific requirements and functionality.