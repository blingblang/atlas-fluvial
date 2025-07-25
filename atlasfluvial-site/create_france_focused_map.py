"""Create a France-focused map with better boundaries."""

import staticmap
import os
from PIL import Image, ImageDraw, ImageFilter

def create_france_focused_map():
    """Create a map focused on France with soft edges for neighboring countries."""
    
    # Create a static map centered on France
    context = staticmap.StaticMap(1600, 1400, 10, 10, 
                                  url_template='https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png')
    
    # Center on France - adjusted for better framing
    center_lat = 46.5
    center_lon = 2.0
    zoom = 6
    
    # Render the map
    image = context.render(zoom=zoom, center=[center_lon, center_lat])
    
    # Convert to PIL Image
    pil_image = image.convert('RGB')
    
    # Create a vignette effect to fade out the edges
    # This creates a more natural focus on France without harsh masking
    width, height = pil_image.size
    
    # Create a gradient mask
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # Create an elliptical gradient centered on France
    # France is roughly in the center of our map
    center_x = width // 2
    center_y = height // 2
    
    # Create concentric ellipses for smooth gradient
    for i in range(255, 0, -2):
        # Adjust these values to control the fade area
        x_radius = int(width * 0.4 * (i / 255.0))
        y_radius = int(height * 0.45 * (i / 255.0))
        
        left = center_x - x_radius
        top = center_y - y_radius
        right = center_x + x_radius
        bottom = center_y + y_radius
        
        draw.ellipse([left, top, right, bottom], fill=i)
    
    # Apply Gaussian blur to smooth the mask
    mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
    
    # Create a white background
    white_bg = Image.new('RGB', (width, height), (250, 250, 250))
    
    # Composite the map over white using the mask
    result = Image.composite(pil_image, white_bg, mask)
    
    # Crop to remove excess white space and center on France
    # These values are approximate based on France's position
    crop_box = (100, 50, width-100, height-50)
    result = result.crop(crop_box)
    
    # Resize to standard dimensions
    result = result.resize((1400, 1200), Image.Resampling.LANCZOS)
    
    # Save the image
    out_dir = os.path.join(os.path.dirname(__file__), 'out')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    output_path = os.path.join(out_dir, 'france-map-grayscale.jpg')
    result.save(output_path, 'JPEG', quality=90)
    print(f"Created France-focused map at {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_france_focused_map()