import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
try:
    from weasyprint import HTML
except ImportError:
    HTML = None  # Handle cases where weasyprint isn't installed in this env

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def render_report_to_pdf(context: dict, output_path: str) -> None:
    """
    Renders the compliance report to a PDF file.
    
    Args:
        context: Dictionary containing 'company_name', 'reporting_period', 
                 'sections', 'signatures', etc.
        output_path: Destination file path for the PDF.
    """
    if HTML is None:
        raise RuntimeError("WeasyPrint is not installed. Application cannot generate PDFs.")

    # 1. Setup Jinja2 Environment
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('report_template.html')
    
    # 2. Add timestamp
    context['generated_at'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # 3. Render HTML
    html_content = template.render(context)
    
    # 4. Generate PDF
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    html_obj = HTML(string=html_content)
    html_obj.write_pdf(output_path)
    
    print(f"PDF generated successfully at {output_path}")

def render_report_to_html(context: dict) -> str:
    """
    For debugging or preview, render just the HTML string.
    """
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('report_template.html')
    context['generated_at'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    return template.render(context)
