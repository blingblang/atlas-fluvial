"""Test navigable waterways map generation."""

from src.pdf_generator.navigable_waterways_generator import create_map_image
from src.pdf_generator.pdf_creator import create_pdf_with_map
import tempfile
import os

# Coordinates
LATITUDE = 47.9797
LONGITUDE = 2.0836

def test_navigable_waterways():
    """Test map generation with only navigable waterways."""
    
    print(f"Generating map with navigable waterways only:")
    print(f"  Northwest corner: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"  Waterways: Vilaine, Brivet, Canal de Nantes à Brest, Erdre, Loire, Sèvre Nantaise, Don")
    
    # Generate map
    map_path = create_map_image(LATITUDE, LONGITUDE, "navigable_waterways_map.png")
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
    test_navigable_waterways()