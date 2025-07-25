"""Debug OSM data fetching."""

import requests
import json

# Display bounds from the map
display_sw_lat, display_sw_lon = 46.965, -2.719
display_ne_lat, display_ne_lon = 47.673, -1.241

bbox = f"{display_sw_lat},{display_sw_lon},{display_ne_lat},{display_ne_lon}"

overpass_url = "https://overpass-api.de/api/interpreter"

query = f"""
[out:json][timeout:30];
(
  way["waterway"="river"]["name"~"Vilaine",i]({bbox});
  relation["waterway"="river"]["name"~"Vilaine",i]({bbox});
);
out geom;
"""

print(f"Query bbox: {bbox}")
print("Sending query to Overpass API...")

response = requests.post(overpass_url, data=query, timeout=30)
if response.status_code == 200:
    data = response.json()
    print(f"\nFound {len(data.get('elements', []))} elements")
    
    # Analyze each element
    for i, element in enumerate(data.get('elements', [])):
        if element.get('type') == 'way' and 'geometry' in element:
            coords = [(node['lat'], node['lon']) for node in element['geometry']]
            if coords:
                lat_min = min(c[0] for c in coords)
                lat_max = max(c[0] for c in coords)
                lon_min = min(c[1] for c in coords)
                lon_max = max(c[1] for c in coords)
                
                print(f"\nWay {i+1}: {len(coords)} points")
                print(f"  Lat range: {lat_min:.3f} to {lat_max:.3f}")
                print(f"  Lon range: {lon_min:.3f} to {lon_max:.3f}")
                print(f"  Name: {element.get('tags', {}).get('name', 'unnamed')}")
                
                # Check how many points are within display bounds
                in_bounds = sum(1 for lat, lon in coords 
                              if display_sw_lat <= lat <= display_ne_lat 
                              and display_sw_lon <= lon <= display_ne_lon)
                print(f"  Points within bounds: {in_bounds}/{len(coords)}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)