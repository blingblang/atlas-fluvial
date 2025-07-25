"""Test waterway rendering in maps."""

from src.pdf_generator.simple_map_generator import create_map_image as create_simple_map
from src.pdf_generator.pdf_creator import create_pdf_with_map
import tempfile
import os

# Coordinates
LATITUDE = 47.9797
LONGITUDE = 2.0836

def test_waterway_map():
    """Test map generation with waterways."""
    
    print(f"Generating map with waterways:")
    print(f"  Northwest corner: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"  Waterways will be shown in light blue")
    
    # Generate map with waterways
    map_path = create_simple_map(LATITUDE, LONGITUDE, "map_with_waterways.png")
    print(f"\nMap created: {map_path}")
    
    # Create PDF
    pdf_path = tempfile.mktemp(suffix='.pdf')
    pdf_path = create_pdf_with_map(map_path, pdf_path)
    print(f"PDF created: {pdf_path}")
    
    # Open the PDF
    if os.name == 'nt':
        os.startfile(pdf_path)
    
    return pdf_path

if __name__ == "__main__":
    test_waterway_map()