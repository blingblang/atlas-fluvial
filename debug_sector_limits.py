"""Debug sector limit positions."""

import json

# Load locks
with open('src/pdf_generator/locks.json', 'r') as f:
    locks_data = json.load(f)

# Map bounds
display_sw_lat, display_sw_lon = 46.965, -2.719
display_ne_lat, display_ne_lon = 47.673, -1.241

print("Map bounds:")
print(f"  SW: {display_sw_lat}, {display_sw_lon}")
print(f"  NE: {display_ne_lat}, {display_ne_lon}")
print()

# Check sector limits
for lock in locks_data['locks']:
    if lock['name'] in ['Arzal', 'Bateliers']:
        lat = lock['latitude']
        lon = lock['longitude']
        slope = lock['slope']
        
        # Check if within bounds
        within = display_sw_lat <= lat <= display_ne_lat and display_sw_lon <= lon <= display_ne_lon
        
        print(f"{lock['name']}:")
        print(f"  Coordinates: {lat}, {lon}")
        print(f"  Slope: {slope}°")
        print(f"  Within bounds: {within}")
        
        if within:
            # Calculate pixel position
            x_ratio = (lon - display_sw_lon) / (display_ne_lon - display_sw_lon)
            y_ratio = 1 - (lat - display_sw_lat) / (display_ne_lat - display_sw_lat)
            print(f"  Position ratios: x={x_ratio:.3f}, y={y_ratio:.3f}")
            print(f"  Approx pixel position (3508x2481): x={int(x_ratio*3508)}, y={int(y_ratio*2481)}")
        print()