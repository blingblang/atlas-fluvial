"""Download a clean France map from Wikimedia."""

import os
import requests
from PIL import Image
from io import BytesIO

def download_clean_france_map():
    """Download a clean map showing just France."""
    
    # Using a Wikimedia Commons France location map
    # This is a clean map showing just France without other countries
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/France_location_map-Regions_and_departements-2016.svg/1200px-France_location_map-Regions_and_departements-2016.svg.png"
    
    try:
        # Download the image
        response = requests.get(url, headers={'User-Agent': 'AtlasFluvial/1.0'})
        response.raise_for_status()
        
        # Open with PIL
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Enhance contrast slightly
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Convert back to RGB for saving as JPEG
        img = img.convert('RGB')
        
        # Resize to our standard size
        img = img.resize((1400, 1200), Image.Resampling.LANCZOS)
        
        # Save
        out_dir = os.path.join(os.path.dirname(__file__), 'out')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        output_path = os.path.join(out_dir, 'france-map-grayscale.jpg')
        img.save(output_path, 'JPEG', quality=90)
        print(f"Downloaded and processed France map at {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"Error downloading map: {e}")
        # Fallback to creating a simple map
        return create_simple_france_map()

def create_simple_france_map():
    """Create a simple outline map of France as fallback."""
    img = Image.new('RGB', (1400, 1200), color='white')
    
    # Save
    out_dir = os.path.join(os.path.dirname(__file__), 'out')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    output_path = os.path.join(out_dir, 'france-map-grayscale.jpg')
    img.save(output_path, 'JPEG', quality=90)
    return output_path

if __name__ == "__main__":
    download_clean_france_map()