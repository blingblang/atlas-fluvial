"""Create an accurate France map using staticmap."""

import staticmap
import os
from PIL import Image, ImageDraw

def create_accurate_france_map():
    """Create an accurate grayscale map of France with neighboring countries masked."""
    
    # Create a static map centered on France
    # France roughly spans from 42°N to 51°N and 5°W to 8°E
    context = staticmap.StaticMap(1400, 1200, 10, 10, 
                                  url_template='https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png')
    
    # Center the map on France (approximately center of the country)
    center_lat = 46.5
    center_lon = 2.0
    zoom = 6  # Zoom level to show all of France
    
    # Render the map
    image = context.render(zoom=zoom, center=[center_lon, center_lat])
    
    # Convert to PIL Image for editing
    pil_image = image.convert('RGB')
    draw = ImageDraw.Draw(pil_image)
    
    # Create semi-transparent white overlay for non-French areas
    # These are approximate pixel coordinates on the 1400x1200 image
    
    # Mask Spain (bottom left)
    spain_mask = [(0, 850), (0, 1200), (600, 1200), (550, 950), (450, 900), (350, 850)]
    draw.polygon(spain_mask, fill=(245, 245, 245))
    
    # Mask Italy (right side)
    italy_mask = [(1050, 500), (1050, 1200), (1400, 1200), (1400, 500)]
    draw.polygon(italy_mask, fill=(245, 245, 245))
    
    # Mask Switzerland (upper right)
    swiss_mask = [(950, 350), (950, 550), (1100, 550), (1100, 350)]
    draw.polygon(swiss_mask, fill=(245, 245, 245))
    
    # Mask Germany (top right)
    germany_mask = [(900, 0), (900, 350), (1400, 350), (1400, 0)]
    draw.polygon(germany_mask, fill=(245, 245, 245))
    
    # Mask Belgium/Luxembourg (top)
    belgium_mask = [(600, 0), (600, 150), (900, 150), (900, 0)]
    draw.polygon(belgium_mask, fill=(245, 245, 245))
    
    # Mask UK (top left - partial)
    uk_mask = [(0, 0), (0, 200), (300, 200), (300, 0)]
    draw.polygon(uk_mask, fill=(245, 245, 245))
    
    # Add subtle border lines around France
    # Western coast is natural (Atlantic)
    # Northern border
    draw.line([(300, 150), (600, 150), (900, 150)], fill=(200, 200, 200), width=2)
    # Eastern border
    draw.line([(900, 150), (950, 350), (950, 550), (1050, 750), (1000, 900)], fill=(200, 200, 200), width=2)
    # Southern border (Pyrenees)
    draw.line([(350, 850), (450, 900), (550, 950), (700, 950)], fill=(200, 200, 200), width=2)
    # Mediterranean coast is natural
    
    # Save the image
    out_dir = os.path.join(os.path.dirname(__file__), 'out')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    output_path = os.path.join(out_dir, 'france-map-grayscale.jpg')
    pil_image.save(output_path, 'JPEG', quality=90)
    print(f"Created accurate France map at {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_accurate_france_map()