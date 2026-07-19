# Invoicing System
The Invoicing System is a comprehensive application designed to manage invoices, clients, products, and coupons for a business. It provides a user-friendly interface for users to log in, view, and manage their data efficiently.

## Key Features
* User authentication and authorization
* Client management
* Product management
* Coupon management
* Invoice generation and management
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
* `app.py`: The main application module, responsible for initializing the application and handling user interactions.
* `database.py`: The database module, responsible for interacting with the database and performing CRUD operations.
* `dialogs`: A package containing various dialog modules, each responsible for a specific type of dialog (e.g., client, product, coupon).
* `models`: A package containing various model modules, each representing a specific entity (e.g., client, product, invoice).
* `templates`: A package containing HTML templates for generating invoices.
* `utils`: A package containing various utility modules, each providing a specific functionality (e.g., configuration management, Excel utilities, invoice generation).
* `views`: A package containing various view modules, each responsible for displaying a specific type of data (e.g., clients, products, invoices).

## Prerequisites and Environment Setup
### System Prerequisites
* Python 3.8 or later
* Tkinter library
* Database library (e.g., MySQL, PostgreSQL)

### Virtual Environment Setup
To set up a virtual environment, follow these steps:
1. Create a new virtual environment using `python -m venv venv`.
2. Activate the virtual environment using `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows).
3. Install the required dependencies using `pip install -r requirements.txt`.

### Configuration
#### Environment Variables
The application requires the following environment variables to be set:
* `DATABASE_URL`: The URL of the database (e.g., `mysql://user:password@host:port/dbname`)
* `WHATSAPP_API_KEY`: The API key for the WhatsApp API

#### JSON Parameter Files
The application uses a JSON file to store configuration parameters. The file should have the following structure:
```json
{
    "database_url": "your_database_url_here",
    "whatsapp_api_key": "your_whatsapp_api_key_here",
    "invoice_template": "/path/to/your/invoice_template.html"
}
```
Replace the placeholder values with your actual database URL, WhatsApp API key, and invoice template path.

## Installation
To install the application, follow these steps:
1. Clone the repository using `git clone https://github.com/your-repo/invoicing-system.git`.
2. Create a new virtual environment and activate it.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Set the environment variables and create the JSON parameter file.

## Usage Example
To run the application, use the following command:
```bash
python main.py
```
This will launch the login window, where you can enter your credentials to access the application.

## Usage Restrictions
* The application requires a valid database connection to function properly.
* The application requires a valid WhatsApp API key to send invoices via WhatsApp.
* The application is designed for use on a desktop environment and may not be compatible with mobile devices.

## Workflow Diagram
```mermaid
graph LR
    A[User] -->|Launches Application| B[Login Window]
    B -->|Enters Credentials| C[Database]
    C -->|Verifies Credentials| D[Main Application]
    D -->|Displays Menu| E[User]
    E -->|Selects Option| F[Dialog]
    F -->|Performs Action| G[Database]
    G -->|Updates Data| H[Main Application]
    H -->|Displays Updated Data| I[User]
    I -->|Logs Out| J[Login Window]
```
Note: This diagram illustrates the basic workflow of the application, from launching the application to logging out.