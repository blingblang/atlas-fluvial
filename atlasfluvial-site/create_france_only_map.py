"""Create a France-only map using a different approach."""

import os
import requests
from PIL import Image
from io import BytesIO

def create_france_only_map():
    """Download a France-focused map from a static map service."""
    
    # Use OpenStreetMap static map API focused on France
    # Alternative approach: use a static map service with country boundaries
    
    # MapBox static API style (would need API key)
    # Or use Stamen Toner which has good country isolation
    
    # For now, let's use a different tile provider that shows cleaner boundaries
    # Using Stamen Toner-Lite for cleaner country separation
    
    import staticmap
    
    # Create map with Stamen Toner-Lite tiles (cleaner country boundaries)
    context = staticmap.StaticMap(1400, 1200, 10, 10, 
                                  url_template='https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png')
    
    # Center on France with appropriate zoom to fill the frame
    center_lat = 46.5
    center_lon = 2.0
    zoom = 6
    
    # Render the map
    image = context.render(zoom=zoom, center=[center_lon, center_lat])
    
    # Convert to grayscale for consistency
    grayscale_image = image.convert('L').convert('RGB')
    
    # Save the image
    out_dir = os.path.join(os.path.dirname(__file__), 'out')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    output_path = os.path.join(out_dir, 'france-map-grayscale.jpg')
    grayscale_image.save(output_path, 'JPEG', quality=90)
    print(f"Created France-only map at {output_path}")
    
    return output_path

def download_france_svg():
    """Alternative: Download a clean SVG map of France."""
    # This would get a clean outline map of just France
    # Could use Natural Earth data or similar
    pass

if __name__ == "__main__":
    create_france_only_map()