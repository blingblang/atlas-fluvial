"""PDF creation module for generating map and culture pages."""

from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from PIL import Image as PILImage
import requests
from io import BytesIO


class PDFGenerator:
    """Generate PDF with map and culture pages."""
    
    def __init__(self):
        self.page_width, self.page_height = A4
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles for the PDF."""
        self.styles.add(ParagraphStyle(
            name='PageTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='DateLabel',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#7f8c8d'),
            alignment=TA_CENTER,
            spaceAfter=20
        ))
    
    def create_map_page(self, map_image_path: str, canvas_obj: canvas.Canvas):
        """Create the map page with label."""
        # Add page title
        canvas_obj.setFont("Helvetica-Bold", 24)
        canvas_obj.drawCentredString(self.page_width / 2, self.page_height - 50, "Map 1")
        
        # Add map image
        if Path(map_image_path).exists():
            # Calculate image position to center it
            img = PILImage.open(map_image_path)
            img_width, img_height = img.size
            
            # Scale to fit page with margins
            max_width = self.page_width - 2 * cm
            max_height = self.page_height - 4 * cm  # Leave space for title
            
            scale = min(max_width / img_width, max_height / img_height)
            scaled_width = img_width * scale
            scaled_height = img_height * scale
            
            x = (self.page_width - scaled_width) / 2
            y = (self.page_height - scaled_height) / 2 - cm
            
            canvas_obj.drawImage(map_image_path, x, y, scaled_width, scaled_height)
    
    def create_culture_page(self, canvas_obj: canvas.Canvas):
        """Create the culture page with 6 sections (2x3 grid)."""
        # Add date at the top
        canvas_obj.setFont("Helvetica", 12)
        date_text = f"Updated on {datetime.now().strftime('%Y-%m-%d')}"
        canvas_obj.drawCentredString(self.page_width / 2, self.page_height - 30, date_text)
        
        # Calculate grid dimensions
        margin = 2 * cm
        grid_width = (self.page_width - 2 * margin) / 2
        grid_height = (self.page_height - 3 * margin) / 3
        
        # Lorem ipsum text
        lorem_ipsum = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
            "Duis aute irure dolor in reprehenderit in voluptate velit.",
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa.",
            "Qui officia deserunt mollit anim id est laborum."
        ]
        
        # Draw 6 sections
        for row in range(3):
            for col in range(2):
                x = margin + col * grid_width
                y = self.page_height - margin - (row + 1) * grid_height - cm
                
                # Draw border
                canvas_obj.rect(x, y, grid_width - 0.5 * cm, grid_height - 0.5 * cm)
                
                # Add lorem ipsum text
                text_idx = row * 2 + col
                canvas_obj.setFont("Helvetica", 10)
                
                # Draw text with word wrap
                text = lorem_ipsum[text_idx]
                text_object = canvas_obj.beginText(x + 0.5 * cm, y + grid_height - cm)
                
                # Simple word wrap
                words = text.split()
                line = ""
                max_width = grid_width - cm
                
                for word in words:
                    test_line = line + word + " "
                    if canvas_obj.stringWidth(test_line, "Helvetica", 10) < max_width:
                        line = test_line
                    else:
                        text_object.textLine(line.strip())
                        line = word + " "
                
                if line:
                    text_object.textLine(line.strip())
                
                canvas_obj.drawText(text_object)
                
                # Add placeholder for image
                img_y = y + 0.5 * cm
                img_height = grid_height * 0.4
                canvas_obj.setFillColor(colors.lightgrey)
                canvas_obj.rect(x + 0.5 * cm, img_y, grid_width - cm, img_height, fill=1)
                canvas_obj.setFillColor(colors.black)
                canvas_obj.drawCentredString(x + grid_width / 2, img_y + img_height / 2, "[Stock Photo]")
    
    def generate_pdf(self, map_image_path: str, output_path: str) -> str:
        """Generate the complete PDF with map and culture pages."""
        c = canvas.Canvas(output_path, pagesize=A4)
        
        # Create map page
        self.create_map_page(map_image_path, c)
        c.showPage()
        
        # Create culture page
        self.create_culture_page(c)
        
        # Save PDF
        c.save()
        return output_path


def create_pdf_with_map(map_image_path: str, output_filename: str = "atlas_document.pdf") -> str:
    """Create a PDF with map and culture pages."""
    generator = PDFGenerator()
    output_path = Path(output_filename)
    return generator.generate_pdf(map_image_path, str(output_path))