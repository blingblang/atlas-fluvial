"""Analyze what content is being rendered on the map."""

import json
from pathlib import Path

def main():
    """Analyze map content."""
    
    # Load configurations
    config_path = Path("src/pdf_generator/map_configurations.json")
    municipalities_path = Path("src/pdf_generator/municipalities.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        map_data = json.load(f)
    
    with open(municipalities_path, 'r', encoding='utf-8') as f:
        muni_data = json.load(f)
    
    # Get Map 1 configuration
    map_1 = next(m for m in map_data['maps'] if m['id'] == 1)
    
    print("Map 1 Configuration:")
    print(f"- Name: {map_1['name']}")
    print(f"- Center: {map_1['center_latitude']}°N, {map_1['center_longitude']}°W")
    print(f"- Scale: 1:{map_1['scale']:,}")
    print(f"- Slope: {map_1['slope']}°")
    
    # Calculate approximate bounds
    from src.pdf_generator.osm_config_map import OSMConfigMapGenerator
    generator = OSMConfigMapGenerator(map_id=1)
    bounds = generator.calculate_map_bounds_from_center()
    
    print(f"\nMap bounds:")
    print(f"- North: {bounds[0]:.4f}°")
    print(f"- West: {bounds[1]:.4f}°")
    print(f"- South: {bounds[2]:.4f}°")
    print(f"- East: {bounds[3]:.4f}°")
    
    # Get cities for Map 1
    cities = [m for m in muni_data['municipalities'] if 1 in m.get('maps', [])]
    
    print(f"\nCities on Map 1: {len(cities)} total")
    
    # Group by type
    major_cities = [c for c in cities if c.get('type') == 'major']
    medium_cities = [c for c in cities if c.get('type') == 'medium']
    small_cities = [c for c in cities if c.get('type') == 'small']
    
    print(f"\nBy type:")
    print(f"- Major cities ({len(major_cities)}): {', '.join(c['name'] for c in major_cities)}")
    print(f"- Medium cities ({len(medium_cities)}): {', '.join(c['name'] for c in medium_cities[:5])}..." if len(medium_cities) > 5 else f"- Medium cities ({len(medium_cities)}): {', '.join(c['name'] for c in medium_cities)}")
    print(f"- Small cities ({len(small_cities)}): {', '.join(c['name'] for c in small_cities[:5])}..." if len(small_cities) > 5 else f"- Small cities ({len(small_cities)}): {', '.join(c['name'] for c in small_cities)}")
    
    # Check which cities are within bounds
    in_bounds = []
    out_bounds = []
    
    for city in cities:
        lat = city['latitude']
        lon = city['longitude']
        if bounds[2] <= lat <= bounds[0] and bounds[1] <= lon <= bounds[3]:
            in_bounds.append(city)
        else:
            out_bounds.append(city)
    
    print(f"\nCities within map bounds: {len(in_bounds)}")
    print(f"Cities outside map bounds: {len(out_bounds)}")
    
    if out_bounds:
        print("\nCities outside bounds:")
        for city in out_bounds[:5]:
            print(f"  - {city['name']} ({city['latitude']:.4f}°N, {city['longitude']:.4f}°W)")
        if len(out_bounds) > 5:
            print(f"  ... and {len(out_bounds) - 5} more")

if __name__ == "__main__":
    main()