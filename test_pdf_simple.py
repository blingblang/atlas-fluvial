"""Simple test for PDF generation without map (to test basic functionality)."""

import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_simple_pdf():
    """Create a simple PDF without the map component."""
    
    # Create temporary file
    output_path = tempfile.mktemp(suffix='.pdf')
    
    # Create PDF
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4
    
    # Page 1: Placeholder for map
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_width / 2, page_height - 50, "Map 1")
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_width / 2, page_height / 2, "[Map will be generated here]")
    c.drawCentredString(page_width / 2, page_height / 2 - 20, "Northwest corner: 47.9797°N, 2.0836°E")
    c.drawCentredString(page_width / 2, page_height / 2 - 40, "Scale: 1:375,000")
    c.showPage()
    
    # Page 2: Culture page
    c.setFont("Helvetica", 12)
    date_text = f"Updated on {datetime.now().strftime('%Y-%m-%d')}"
    c.drawCentredString(page_width / 2, page_height - 30, date_text)
    
    # Draw 6 sections
    margin = 2 * 28.35  # 2 cm in points
    grid_width = (page_width - 2 * margin) / 2
    grid_height = (page_height - 3 * margin) / 3
    
    lorem_ipsum = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco.",
        "Duis aute irure dolor in reprehenderit in voluptate velit.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa.",
        "Qui officia deserunt mollit anim id est laborum."
    ]
    
    for row in range(3):
        for col in range(2):
            x = margin + col * grid_width
            y = page_height - margin - (row + 1) * grid_height - 28.35
            
            # Draw border
            c.rect(x, y, grid_width - 14.17, grid_height - 14.17)
            
            # Add text
            text_idx = row * 2 + col
            c.setFont("Helvetica", 10)
            c.drawString(x + 14.17, y + grid_height - 28.35, lorem_ipsum[text_idx])
    
    # Save PDF
    c.save()
    
    print(f"Simple PDF created successfully!")
    print(f"Location: {output_path}")
    print(f"Size: {os.path.getsize(output_path)} bytes")
    
    return output_path

if __name__ == "__main__":
    print("Creating simple PDF (without map)...")
    create_simple_pdf()