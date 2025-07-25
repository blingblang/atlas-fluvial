"""Test Nantes environs map generation."""

from src.pdf_generator.nantes_environs_map import create_map_image
from src.pdf_generator.pdf_creator import create_pdf_with_map
import tempfile
import os

# Coordinates
LATITUDE = 47.9797
LONGITUDE = 2.0836

def test_nantes_map():
    """Test Nantes environs map generation with all features."""
    
    print(f"Generating Nantes and environs map:")
    print(f"  Northwest corner: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"  Features:")
    print(f"    - Atlantic Ocean (light blue)")
    print(f"    - Waterways: Vilaine, Brivet, Canal de Nantes à Brest, Erdre,")
    print(f"                 Loire, Sèvre Nantaise, Don, Saint Eloi")
    print(f"    - Motorway: N165")
    print(f"    - City: Nantes")
    
    # Generate map
    map_path = create_map_image(LATITUDE, LONGITUDE, "nantes_environs_map.png")
    print(f"\nMap created: {map_path}")
    
    # Create PDF
    pdf_path = tempfile.mktemp(suffix='.pdf')
    pdf_path = create_pdf_with_map(map_path, pdf_path)
    print(f"PDF created: {pdf_path}")
    print(f"Map label: '1: Nantes and environs'")
    
    # Open the PDF
    if os.name == 'nt':
        os.startfile(pdf_path)
    
    return pdf_path

if __name__ == "__main__":
    test_nantes_map()