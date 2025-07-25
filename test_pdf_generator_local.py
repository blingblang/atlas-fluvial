"""Test PDF generation locally without Netlify upload."""

import os
import tempfile
from src.pdf_generator.simple_map_generator import create_map_image
from src.pdf_generator.pdf_creator import create_pdf_with_map

# Coordinates
LATITUDE = 47.9797  # Northwest corner latitude
LONGITUDE = 2.0836  # Northwest corner longitude

def test_local_generation():
    """Test PDF generation without uploading to Netlify."""
    
    print(f"Generating PDF with map from coordinates:")
    print(f"  Northwest corner: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"  Scale: 1:375,000")
    print(f"  Paper size: A4")
    
    # Step 1: Generate map
    print("\n1. Generating map...")
    map_path = create_map_image(LATITUDE, LONGITUDE)
    print(f"   Map created: {map_path}")
    print(f"   Size: {os.path.getsize(map_path)} bytes")
    
    # Step 2: Create PDF
    print("\n2. Creating PDF...")
    pdf_path = tempfile.mktemp(suffix='.pdf')
    pdf_path = create_pdf_with_map(map_path, pdf_path)
    print(f"   PDF created: {pdf_path}")
    print(f"   Size: {os.path.getsize(pdf_path)} bytes")
    
    print("\nPDF generated successfully!")
    print(f"Open the file to view: {pdf_path}")
    
    # Open the PDF (Windows)
    if os.name == 'nt':
        os.startfile(pdf_path)
    
    return pdf_path

if __name__ == "__main__":
    test_local_generation()