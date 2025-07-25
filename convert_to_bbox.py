"""Convert center-based map configs to bounding box format."""

import json
import math
from pathlib import Path

def calculate_bbox_from_center(center_lat, center_lon, scale):
    """Calculate bounding box from center and scale."""
    # A4 landscape dimensions
    paper_width_mm = 297
    paper_height_mm = 210
    
    # Convert to meters
    paper_width_m = (paper_width_mm / 1000) * scale
    paper_height_m = (paper_height_mm / 1000) * scale
    
    # Earth's radius in meters
    earth_radius = 6371000
    
    # Calculate half spans
    half_lat_span = (paper_height_m / 2) / earth_radius * (180 / math.pi)
    half_lon_span = (paper_width_m / 2) / (earth_radius * math.cos(math.radians(center_lat))) * (180 / math.pi)
    
    # Calculate corners
    sw_lat = center_lat - half_lat_span
    ne_lat = center_lat + half_lat_span
    sw_lon = center_lon - half_lon_span
    ne_lon = center_lon + half_lon_span
    
    return sw_lat, sw_lon, ne_lat, ne_lon

def main():
    """Convert map configurations."""
    config_path = Path("src/pdf_generator/map_configurations.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert each map
    new_maps = []
    for map_config in data['maps']:
        if 'center_latitude' in map_config:
            # Calculate bounding box
            center_lat = map_config['center_latitude']
            center_lon = map_config['center_longitude']
            scale = map_config.get('scale', 375000)
            
            sw_lat, sw_lon, ne_lat, ne_lon = calculate_bbox_from_center(center_lat, center_lon, scale)
            
            # Create new format
            new_map = {
                "id": map_config['id'],
                "name": map_config['name'],
                "southwest_corner": {
                    "latitude": round(sw_lat, 4),
                    "longitude": round(sw_lon, 4)
                },
                "northeast_corner": {
                    "latitude": round(ne_lat, 4),
                    "longitude": round(ne_lon, 4)
                },
                "description": map_config.get('description', '')
            }
            
            # Add slope if it exists and is non-zero
            if map_config.get('slope', 0) != 0:
                new_map['slope'] = map_config['slope']
            
            new_maps.append(new_map)
            
            print(f"Map {map_config['id']}: {map_config['name']}")
            print(f"  Old: center=({center_lat}, {center_lon}), scale={scale}")
            print(f"  New: SW=({sw_lat:.4f}, {sw_lon:.4f}), NE=({ne_lat:.4f}, {ne_lon:.4f})")
        else:
            # Already in new format
            new_maps.append(map_config)
    
    # Save new format
    new_data = {"maps": new_maps}
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nConverted {len(new_maps)} maps to bounding box format")

if __name__ == "__main__":
    main()