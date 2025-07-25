"""Create a placeholder France map image."""

from PIL import Image, ImageDraw, ImageFont
import os

def create_france_map_placeholder():
    """Create a more accurate grayscale France map placeholder."""
    
    # Create a larger image for better quality
    width, height = 1400, 1200
    img = Image.new('RGB', (width, height), color='#f5f5f5')
    draw = ImageDraw.Draw(img)
    
    # Draw water bodies first (Atlantic Ocean and Mediterranean)
    # Atlantic Ocean (left side)
    atlantic_points = [
        (0, 0), (0, height), (300, height), (250, 900), (200, 750), 
        (150, 600), (100, 450), (150, 300), (200, 150), (250, 50), (300, 0)
    ]
    draw.polygon(atlantic_points, fill='#e0e0e0')
    
    # Mediterranean Sea (bottom right)
    mediterranean_points = [
        (800, height), (width, height), (width, 850), (1200, 900), 
        (1000, 950), (800, 1000), (800, height)
    ]
    draw.polygon(mediterranean_points, fill='#e0e0e0')
    
    # Draw more accurate France outline
    france_outline = [
        # Northern coast
        (700, 50),    # Dunkirk area
        (600, 60),    # Calais
        (500, 80),    # Normandy coast
        (400, 120),   # Cherbourg area
        (350, 180),   # Brittany north
        
        # Brittany peninsula
        (280, 250),   # Brest area
        (270, 350),   # Brittany west
        (300, 420),   # Brittany south
        (350, 450),   # Lorient area
        (400, 480),   # Nantes area
        
        # Atlantic coast
        (380, 550),   # La Rochelle area
        (370, 650),   # Bordeaux area
        (380, 750),   # Biarritz area
        (450, 850),   # Pyrenees west
        
        # Mediterranean coast
        (550, 900),   # Perpignan area
        (650, 920),   # Montpellier area
        (750, 930),   # Marseille area
        (850, 920),   # Toulon area
        (950, 900),   # Nice area
        (1000, 850),  # Italian border
        
        # Eastern border
        (1050, 750),  # Alps
        (1100, 600),  # Geneva area
        (1120, 450),  # Basel area
        (1100, 300),  # Strasbourg area
        (1050, 150),  # Luxembourg area
        
        # Northern border
        (950, 80),    # Belgium border
        (800, 50),    # Lille area
        (700, 50),    # Back to start
    ]
    
    # Draw France with better color
    draw.polygon(france_outline, fill='#ffffff', outline='#888888', width=2)
    
    # Add some topographical shading for mountains
    # Alps
    alps_points = [(950, 750), (1000, 700), (1050, 650), (1000, 800), (950, 750)]
    draw.polygon(alps_points, fill='#f0f0f0')
    
    # Pyrenees
    pyrenees_points = [(450, 850), (650, 830), (600, 880), (500, 900), (450, 850)]
    draw.polygon(pyrenees_points, fill='#f0f0f0')
    
    # Draw major rivers
    # Seine
    draw.line([(700, 250), (650, 220), (600, 200), (500, 180)], fill='#b0b0b0', width=3)
    
    # Loire (including Nantes area)
    draw.line([(750, 400), (650, 420), (550, 440), (450, 460), (400, 480)], fill='#b0b0b0', width=3)
    
    # Rhône
    draw.line([(900, 550), (850, 650), (800, 750), (750, 850)], fill='#b0b0b0', width=3)
    
    # Garonne
    draw.line([(600, 600), (500, 650), (400, 700)], fill='#b0b0b0', width=3)
    
    # Add text labels for water bodies
    try:
        # Try to use a default font
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    # Label Atlantic Ocean
    draw.text((100, 400), "Atlantic\nOcean", fill='#666666', font=font)
    
    # Label Mediterranean Sea  
    draw.text((950, 950), "Mediterranean Sea", fill='#666666', font=font)
    
    # Mark major cities with dots
    cities = [
        (650, 200, "Paris"),
        (400, 480, "Nantes"),  # Nantes position
        (900, 600, "Lyon"),
        (550, 780, "Toulouse"),
        (400, 650, "Bordeaux"),
        (800, 850, "Marseille"),
        (950, 880, "Nice"),
        (800, 80, "Lille"),
        (1080, 300, "Strasbourg"),
        (350, 300, "Rennes"),
    ]
    
    for x, y, name in cities:
        # City dot
        draw.ellipse([(x-4, y-4), (x+4, y+4)], fill='#444444')
        # City name (optional, might clutter the map)
        # draw.text((x+10, y-5), name, fill='#666666', font=font)
    
    # Save the image
    out_dir = os.path.join(os.path.dirname(__file__), 'out')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    img.save(os.path.join(out_dir, 'france-map-grayscale.jpg'), 'JPEG', quality=90)
    print(f"Created improved France map at {os.path.join(out_dir, 'france-map-grayscale.jpg')}")

if __name__ == "__main__":
    create_france_map_placeholder()