"""Test OSM map generation with detailed debugging."""

from src.pdf_generator.fixed_scale_map import FixedScaleMapGenerator
import tempfile

# Create generator
generator = FixedScaleMapGenerator(map_id=1)

# Override the fetch method to see what's happening
original_fetch = generator._fetch_vilaine_geometry

def debug_fetch():
    """Fetch with detailed debugging."""
    import requests
    
    overpass_url = "https://overpass-api.de/api/interpreter"
    display_sw_lat, display_sw_lon, display_ne_lat, display_ne_lon = generator.display_bounds
    bbox = f"{display_sw_lat},{display_sw_lon},{display_ne_lat},{display_ne_lon}"
    
    query = f"""
    [out:json][timeout:30];
    (
      way["waterway"="river"]["name"~"Vilaine",i]({bbox});
      relation["waterway"="river"]["name"~"Vilaine",i]({bbox});
    );
    out geom;
    """
    
    try:
        response = requests.post(overpass_url, data=query, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            # Collect all segments
            segments = []
            for element in data.get('elements', []):
                if element.get('type') == 'way' and 'geometry' in element:
                    segment = [(node['lat'], node['lon']) for node in element['geometry']]
                    if segment:
                        segments.append(segment)
            
            print(f"\nCollected {len(segments)} segments")
            
            # Show segment details
            total_points = 0
            for i, seg in enumerate(segments):
                total_points += len(seg)
                print(f"Segment {i+1}: {len(seg)} points, "
                      f"lat {min(p[0] for p in seg):.3f}-{max(p[0] for p in seg):.3f}, "
                      f"lon {min(p[1] for p in seg):.3f}-{max(p[1] for p in seg):.3f}")
            
            print(f"\nTotal points before merging: {total_points}")
            
            # Merge segments
            if segments:
                merged = generator._merge_river_segments(segments)
                print(f"After merging: {len(merged)} points")
                
                if merged:
                    # Check for straight line issue
                    lats = [p[0] for p in merged]
                    lons = [p[1] for p in merged]
                    lat_variance = max(lats) - min(lats)
                    lon_variance = max(lons) - min(lons)
                    
                    print(f"\nMerged river stats:")
                    print(f"  Lat range: {min(lats):.3f} to {max(lats):.3f} (variance: {lat_variance:.3f})")
                    print(f"  Lon range: {min(lons):.3f} to {max(lons):.3f} (variance: {lon_variance:.3f})")
                    
                    # Sample some points
                    print(f"\nFirst 5 points: {merged[:5]}")
                    print(f"Last 5 points: {merged[-5:]}")
                
                return merged
    except Exception as e:
        print(f"Error: {e}")
    
    return []

# Replace the method temporarily
generator._fetch_vilaine_geometry = debug_fetch

# Generate map
output_path = tempfile.mktemp(suffix='.png')
result = generator.generate_map(output_path)
print(f"\nMap saved to: {result}")