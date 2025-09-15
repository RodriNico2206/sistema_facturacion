import os
from jinja2 import Template
from xhtml2pdf import pisa
from io import BytesIO
import traceback

class InvoiceGenerator:
    def __init__(self):
        self.template_path = "templates/invoice_template.html"
    
    def generate_invoice(self, factura, output_path="facturas"):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            template = Template(template_content)
            html_content = template.render(factura=factura)
            
            output_file = os.path.join(output_path, f"factura_{factura.numero_factura}.pdf")
            
            # Generar PDF usando xhtml2pdf en lugar de WeasyPrint
            with open(output_file, "w+b") as output_file_handle:
                pisa_status = pisa.CreatePDF(
                    html_content, 
                    dest=output_file_handle,
                    encoding='utf-8'
                )
            
            if pisa_status.err:
                raise Exception(f"Error generando PDF: {pisa_status.err}")
            
            return output_file
            
        except Exception as e:
            print(f"Error generating invoice: {str(e)}")
            print(traceback.format_exc())
            raise