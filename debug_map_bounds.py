"""Debug map bounds and projection."""

import staticmap
from src.pdf_generator.fixed_scale_map import FixedScaleMapGenerator

# Create generator
gen = FixedScaleMapGenerator(map_id=1)

print(f"Generator display bounds: {gen.display_bounds}")
print(f"Center: {gen.center_lat}, {gen.center_lon}")
print(f"Zoom level: {gen.zoom_level}")
print(f"Image size: {gen.width}x{gen.height}")

# Create a staticmap context
context = staticmap.StaticMap(gen.width, gen.height)

# Check what bounds staticmap actually uses
# Unfortunately staticmap doesn't expose the actual bounds it renders
# But we can calculate what it should be

# At zoom level Z, the world is divided into 2^Z x 2^Z tiles
# Each tile is 256x256 pixels
# The number of pixels representing the whole world at zoom Z is 256 * 2^Z

pixels_per_world = 256 * (2 ** gen.zoom_level)
pixels_per_degree_lon = pixels_per_world / 360

# At the equator, pixels per degree latitude is the same
# But it varies with latitude due to Mercator projection
import math

def lat_to_mercator_y(lat):
    """Convert latitude to Mercator Y coordinate."""
    lat_rad = math.radians(lat)
    return math.log(math.tan(math.pi/4 + lat_rad/2))

def mercator_y_to_lat(y):
    """Convert Mercator Y coordinate to latitude."""
    return math.degrees(2 * math.atan(math.exp(y)) - math.pi/2)

# Calculate the Mercator Y bounds for our center point
center_y = lat_to_mercator_y(gen.center_lat)

# The height in Mercator units depends on the zoom level and image height
mercator_height = gen.height / pixels_per_world * 2 * math.pi
mercator_top = center_y + mercator_height / 2
mercator_bottom = center_y - mercator_height / 2

# Convert back to latitude
actual_north_lat = mercator_y_to_lat(mercator_top)
actual_south_lat = mercator_y_to_lat(mercator_bottom)

# Longitude is simpler - linear in Mercator
lon_width = gen.width / pixels_per_degree_lon
actual_west_lon = gen.center_lon - lon_width / 2
actual_east_lon = gen.center_lon + lon_width / 2

print(f"\nActual rendered bounds (estimated):")
print(f"  SW: {actual_south_lat:.6f}, {actual_west_lon:.6f}")
print(f"  NE: {actual_north_lat:.6f}, {actual_east_lon:.6f}")

print(f"\nDifference from display bounds:")
print(f"  South diff: {actual_south_lat - gen.display_bounds[0]:.6f}")
print(f"  West diff: {actual_west_lon - gen.display_bounds[1]:.6f}")
print(f"  North diff: {actual_north_lat - gen.display_bounds[2]:.6f}")
print(f"  East diff: {actual_east_lon - gen.display_bounds[3]:.6f}")