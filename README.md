# Invoicing System
The Invoicing System is a comprehensive application designed to manage invoices, clients, products, and configurations for a business. It provides a user-friendly interface for users to log in, view and manage data, and generate invoices.

## Key Features
* User authentication and authorization
* Client management
* Product management
* Invoice generation and management
* Configuration management
* Integration with Excel and PDF for report generation
* WhatsApp integration for notification sending

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
The Invoicing System consists of several modules that interact with each other to provide a comprehensive invoicing solution. The `main.py` file serves as the entry point of the application, responsible for initializing the database, login window, and the main application window. The `database.py` file handles database operations, while the `models` folder contains classes that represent the data structures used in the application. The `dialogs` folder contains classes that handle user interactions, such as client and product management. The `utils` folder contains utility classes that provide functionality for tasks such as invoice generation, PDF conversion, and WhatsApp notification sending. The `views` folder contains classes that handle the user interface and user interactions.

## Prerequisites and Installation
To run the Invoicing System, you will need to have Python 3.x installed, along with the following libraries:
* `tkinter` for the graphical user interface
* `sqlite3` for database operations
* `openpyxl` for Excel report generation
* `fpdf` for PDF report generation
* `twilio` for WhatsApp notification sending

You can install these libraries using pip:
```bash
pip install tkinter sqlite3 openpyxl fpdf twilio
```

## Usage Example
To run the Invoicing System, simply execute the `main.py` file:
```python
python main.py
```
This will launch the login window, where you can enter your credentials to access the main application window.

## Usage Restrictions
The Invoicing System is designed to run on a local machine, and it requires a database to be set up and configured properly. The system also requires a valid WhatsApp account to send notifications. Additionally, the system may have limitations and constraints due to the use of third-party libraries and services.

## Workflow Diagram
```mermaid
graph LR
    A[User] -->|Login|> B[Login Window]
    B -->|Authenticate|> C[Database]
    C -->|Authorize|> D[Main Application Window]
    D -->|Manage Clients|> E[Client Management]
    D -->|Manage Products|> F[Product Management]
    D -->|Generate Invoices|> G[Invoice Generation]
    G -->|Send Notifications|> H[WhatsApp Notification]
    H -->|Send Reports|> I[Report Generation]
```