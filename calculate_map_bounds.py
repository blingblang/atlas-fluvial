"""Calculate the exact bounds of the map."""

import math

# Given parameters
nw_lat = 47.9797
nw_lon = 2.0836
scale = 375000  # 1:375,000
paper_size = (210, 297)  # A4 in mm

# Convert paper dimensions to meters
paper_width_m = (paper_size[0] / 1000) * scale  # mm to m, then scale
paper_height_m = (paper_size[1] / 1000) * scale

print(f"Map dimensions at 1:{scale:,} scale:")
print(f"Width: {paper_width_m:,.0f} meters ({paper_width_m/1000:.1f} km)")
print(f"Height: {paper_height_m:,.0f} meters ({paper_height_m/1000:.1f} km)")

# Earth's radius in meters
earth_radius = 6371000

# Calculate latitude change (moving south)
lat_change = (paper_height_m / earth_radius) * (180 / math.pi)
se_lat = nw_lat - lat_change

# Calculate longitude change (moving east)
avg_lat = (nw_lat + se_lat) / 2
lon_change = (paper_width_m / (earth_radius * math.cos(math.radians(avg_lat)))) * (180 / math.pi)
se_lon = nw_lon + lon_change

# All four corners
ne_lat = nw_lat
ne_lon = se_lon
sw_lat = se_lat
sw_lon = nw_lon

print(f"\nMap corners:")
print(f"Northwest: {nw_lat:.4f}°N, {nw_lon:.4f}°E")
print(f"Northeast: {ne_lat:.4f}°N, {ne_lon:.4f}°E") 
print(f"Southwest: {sw_lat:.4f}°N, {sw_lon:.4f}°E")
print(f"Southeast: {se_lat:.4f}°N, {se_lon:.4f}°E")

print(f"\nLatitude span: {lat_change:.4f}° ({lat_change * 111:.1f} km)")
print(f"Longitude span: {lon_change:.4f}° ({lon_change * 111 * math.cos(math.radians(avg_lat)):.1f} km)")

# Check if Nantes and waterways fall within these bounds
print(f"\nChecking if key features fall within map bounds:")
features = {
    "Nantes": (47.2184, -1.5536),
    "Loire mouth": (47.2800, -2.2000),
    "Vilaine mouth": (47.5089, -2.5147),
    "Saint-Nazaire": (47.2733, -2.2134)
}

for name, (lat, lon) in features.items():
    in_bounds = sw_lat <= lat <= nw_lat and nw_lon <= lon <= se_lon
    print(f"{name}: {lat:.4f}°N, {lon:.4f}°E - {'INSIDE' if in_bounds else 'OUTSIDE'} map bounds")