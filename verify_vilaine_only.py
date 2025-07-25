"""Verify that only Vilaine river is being rendered."""

from src.pdf_generator.osm_config_map import OSMConfigMapGenerator

def main():
    """Check waterway rendering."""
    
    print("Checking waterway data for Map 1...")
    
    generator = OSMConfigMapGenerator(map_id=1)
    bounds = generator.calculate_map_bounds_from_center()
    
    # Get waterway data
    waterways = generator.fetch_waterways_from_osm(bounds)
    
    print(f"\nWaterways found: {len(waterways)}")
    for name, coords in waterways.items():
        print(f"- {name}: {len(coords)} points")
        if coords:
            print(f"  First point: {coords[0]}")
            print(f"  Last point: {coords[-1]}")
    
    # Check if Vilaine is within map bounds
    if 'Vilaine' in waterways:
        vilaine_coords = waterways['Vilaine']
        in_bounds_count = 0
        for lat, lon in vilaine_coords:
            if bounds[2] <= lat <= bounds[0] and bounds[1] <= lon <= bounds[3]:
                in_bounds_count += 1
        print(f"\nVilaine points within map bounds: {in_bounds_count}/{len(vilaine_coords)}")

if __name__ == "__main__":
    main()