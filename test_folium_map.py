"""Test Folium-based map generation."""

from src.pdf_generator.simple_folium_map import SimpleFoliumMapGenerator

def main():
    """Test the Folium map generator."""
    
    print("Generating Map 1 with Folium (real map tiles)...")
    print("This will create an HTML file that shows the actual geography.")
    
    generator = SimpleFoliumMapGenerator(map_id=1)
    output_path = generator.generate_map("map1_folium.html")
    
    print(f"\nMap generated successfully!")
    print(f"Open this file in your browser to see the map: {output_path}")
    print("\nThe map shows:")
    print("- Real OpenStreetMap data with accurate coastlines")
    print("- The Atlantic Ocean in its actual position")
    print("- All cities with markers (red=major, blue=medium, gray=small)")
    print("- Option to switch to satellite view")
    print("- Interactive zoom and pan")

if __name__ == "__main__":
    main()