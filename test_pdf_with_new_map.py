"""Test PDF generation with freshly generated map."""

import os
from src.pdf_generator.nantes_environs_map import create_map_image
from src.pdf_generator.pdf_creator import create_pdf_with_map

# Coordinates for Nantes
LATITUDE = 47.9797
LONGITUDE = 2.0836

def test_pdf_generation():
    """Test PDF generation with fresh map."""
    
    print("Step 1: Generating map...")
    map_path = create_map_image(LATITUDE, LONGITUDE, "test_map_fresh.png")
    print(f"Map created: {map_path}")
    print(f"Map file size: {os.path.getsize(map_path)} bytes")
    
    print("\nStep 2: Creating PDF...")
    pdf_path = create_pdf_with_map(map_path, "nantes_guide_final.pdf")
    print(f"PDF created: {pdf_path}")
    print(f"PDF file size: {os.path.getsize(pdf_path)} bytes")
    
    # Try to open the PDF
    if os.name == 'nt':
        print("\nOpening PDF...")
        os.startfile(pdf_path)
    
    return pdf_path, map_path

if __name__ == "__main__":
    test_pdf_generation()