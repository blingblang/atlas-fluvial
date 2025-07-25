"""Test map generation locally without uploading."""

from src.pdf_generator.osm_config_map import OSMConfigMapGenerator

def main():
    """Generate and save map locally for inspection."""
    
    print("Generating Map 1 locally...")
    generator = OSMConfigMapGenerator(map_id=1)
    
    # Generate map and save locally
    output_path = "test_map_output.png"
    generator.generate_map(output_path)
    
    print(f"Map saved to: {output_path}")
    print("Please inspect the map to verify:")
    print("1. Only Vilaine river is shown (no extra lines)")
    print("2. All 48 cities are rendered properly")
    print("3. Atlantic Ocean is visible on the west")
    print("4. N165 motorway is shown")

if __name__ == "__main__":
    main()