"""PDF creation module for generating map and culture pages."""

from datetime import datetime
from pathlib import Path
from typing import Tuple, Optional
import tempfile

from reportlab.lib.pagesizes import A4, landscape
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
        self.page_width, self.page_height = landscape(A4)
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
        canvas_obj.drawCentredString(self.page_width / 2, self.page_height - 50, "1: Nantes and environs")
        
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
        
        # Section titles and content for Nantes
        sections = [
            {
                "title": "Bars/Cafes",
                "content": "Le Lieu Unique, housed in the former LU biscuit factory, offers a unique blend of bar, café, and cultural center with its famous curved tower. "
                          "La Cigale brasserie on Place Graslin has been serving locals since 1895 with its ornate Belle Époque interior. "
                          "Café du Commerce near the Château provides riverside terrace seating with views of the Loire."
            },
            {
                "title": "Groceries",
                "content": "The Marché de Talensac is Nantes' largest covered market, operating Tuesday through Sunday with fresh local produce and seafood. "
                          "Passage Pommeraye houses specialty food shops in a stunning 19th-century shopping arcade. "
                          "For waterway provisions, the Carrefour Market on Quai de la Fosse stays open until 9 PM and caters to boaters."
            },
            {
                "title": "Public Safety",
                "content": "The Port Captain's office at Quai Ernest Renaud monitors VHF Channel 9 for emergencies on the Loire. "
                          "Emergency services can be reached at 112, with the nearest hospital being CHU Nantes along the tramway Line 1. "
                          "The river police patrol regularly between Trentemoult and the city center, especially during summer months."
            },
            {
                "title": "Upcoming Events",
                "content": "Le Voyage à Nantes transforms the city into an open-air gallery each summer from July to September. "
                          "The Rendez-vous de l'Erdre jazz festival brings floating stages to the river every August. "
                          "Les Machines de l'île hosts special nighttime events on the first Friday of each month."
            },
            {
                "title": "Local Customs",
                "content": "Nantais traditionally greet with 'Salut' rather than 'Bonjour' in casual settings, reflecting the city's maritime heritage. "
                          "It's customary to buy a round of Muscadet wine when mooring at local yacht clubs along the Erdre. "
                          "Shops close between noon and 2 PM, and most restaurants don't serve dinner before 7:30 PM."
            },
            {
                "title": "Trivia",
                "content": "Jules Verne was born in Nantes in 1828, and his childhood home on Île Feydeau inspired his maritime adventures. "
                          "The city was once called 'Venice of the West' due to its many river channels, most now filled in. "
                          "Petit-Beurre LU cookies have 52 teeth representing weeks of the year and 24 holes for hours in a day."
            }
        ]
        
        # Draw 6 sections
        for row in range(3):
            for col in range(2):
                x = margin + col * grid_width
                y = self.page_height - margin - (row + 1) * grid_height - cm
                
                # Draw border
                canvas_obj.rect(x, y, grid_width - 0.5 * cm, grid_height - 0.5 * cm)
                
                # Get section data
                section_idx = row * 2 + col
                section = sections[section_idx]
                
                # Add section title
                canvas_obj.setFont("Helvetica-Bold", 12)
                canvas_obj.drawString(x + 0.5 * cm, y + grid_height - 0.8 * cm, section["title"])
                
                # Add section content
                canvas_obj.setFont("Helvetica", 9)
                text_object = canvas_obj.beginText(x + 0.5 * cm, y + grid_height - 1.5 * cm)
                
                # Word wrap the content
                words = section["content"].split()
                line = ""
                max_width = grid_width - cm
                line_height = 12
                lines_drawn = 0
                max_lines = int((grid_height - 2 * cm) / line_height)
                
                for word in words:
                    test_line = line + word + " "
                    if canvas_obj.stringWidth(test_line, "Helvetica", 9) < max_width:
                        line = test_line
                    else:
                        if lines_drawn < max_lines:
                            text_object.textLine(line.strip())
                            lines_drawn += 1
                        line = word + " "
                
                if line and lines_drawn < max_lines:
                    text_object.textLine(line.strip())
                
                canvas_obj.drawText(text_object)
    
    def generate_pdf(self, map_image_path: str, output_path: str) -> str:
        """Generate the complete PDF with map and culture pages."""
        c = canvas.Canvas(output_path, pagesize=landscape(A4))
        
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