"""Generate static map images using Folium with staticmap fallback."""

import folium
import json
from pathlib import Path
import tempfile
from typing import Dict, List, Optional
from PIL import Image, ImageDraw, ImageFont
import staticmap
import requests


class StaticFoliumMapGenerator:
    """Generate static map images from Folium or using staticmap."""
    
    def __init__(self, map_id: int = 1):
        self.map_id = map_id
        self.map_config = self._load_map_configuration()
        self.municipalities = self._load_municipalities()
        
        # Extract configuration - now using bounding box
        sw_corner = self.map_config['southwest_corner']
        ne_corner = self.map_config['northeast_corner']
        
        self.sw_lat = sw_corner['latitude']
        self.sw_lon = sw_corner['longitude']
        self.ne_lat = ne_corner['latitude']
        self.ne_lon = ne_corner['longitude']
        
        # Calculate center from bounding box
        self.center_lat = (self.sw_lat + self.ne_lat) / 2
        self.center_lon = (self.sw_lon + self.ne_lon) / 2
        
        self.map_name = self.map_config['name']
        
        # A4 landscape at 300 DPI
        self.width = 3508
        self.height = 2480
        
        # Calculate zoom level based on bounding box span
        lat_span = self.ne_lat - self.sw_lat
        lon_span = self.ne_lon - self.sw_lon
        max_span = max(lat_span, lon_span)
        
        # Approximate zoom level from span
        if max_span > 2:
            self.zoom_level = 8
        elif max_span > 1:
            self.zoom_level = 9
        elif max_span > 0.5:
            self.zoom_level = 10
        elif max_span > 0.25:
            self.zoom_level = 11
        elif max_span > 0.125:
            self.zoom_level = 12
        elif max_span > 0.0625:
            self.zoom_level = 13
        else:
            self.zoom_level = 14
    
    def _load_map_configuration(self) -> Dict:
        """Load map configuration from JSON file."""
        json_path = Path(__file__).parent / "map_configurations.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            maps = data.get('maps', [])
            for map_config in maps:
                if map_config['id'] == self.map_id:
                    return map_config
            
            return {
                'id': self.map_id,
                'name': f'Map {self.map_id}',
                'southwest_corner': {'latitude': 47.0, 'longitude': -2.6},
                'northeast_corner': {'latitude': 48.0, 'longitude': -0.8}
            }
    
    def _load_municipalities(self) -> List[Dict]:
        """Load municipalities from JSON file."""
        json_path = Path(__file__).parent / "municipalities.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('municipalities', [])
    
    def _filter_municipalities_for_map(self) -> List[Dict]:
        """Filter municipalities that should appear on this map."""
        return [m for m in self.municipalities if self.map_id in m.get('maps', [])]
    
    def generate_map_with_staticmap(self, output_path: str) -> str:
        """Generate map using staticmap library."""
        # Create context
        context = staticmap.StaticMap(self.width, self.height, url_template='https://a.tile.openstreetmap.org/{z}/{x}/{y}.png')
        
        # Add cities as markers
        cities = self._filter_municipalities_for_map()
        for city in cities:
            city_type = city.get('type', 'small')
            if city_type == 'major':
                color = 'red'
                size = 12
            elif city_type == 'medium':
                color = 'blue'
                size = 8
            else:
                color = 'gray'
                size = 6
            
            marker = staticmap.CircleMarker(
                (city['longitude'], city['latitude']),
                color,
                size
            )
            context.add_marker(marker)
        
        # Render image
        image = context.render(zoom=self.zoom_level, center=[self.center_lon, self.center_lat])
        
        # Add labels and border
        draw = ImageDraw.Draw(image)
        
        # Try to load fonts
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            info_font = ImageFont.truetype("arial.ttf", 36)
            city_font = ImageFont.truetype("arial.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
            city_font = ImageFont.load_default()
        
        # Add title with background
        title_text = f"{self.map_id}: {self.map_name}"
        draw.rectangle([(20, 20), (800, 100)], fill='white', outline='black', width=3)
        draw.text((40, 40), title_text, fill='black', font=title_font)
        
        # Calculate approximate scale from bounding box
        import math
        earth_radius = 6371000  # meters
        lat_span = self.ne_lat - self.sw_lat
        lon_span = self.ne_lon - self.sw_lon
        
        # Calculate distance in meters for the width of the map
        avg_lat = (self.sw_lat + self.ne_lat) / 2
        width_m = lon_span * earth_radius * math.cos(math.radians(avg_lat)) * math.pi / 180
        
        # A4 width is 297mm
        scale = int(width_m / 0.297)
        
        # Add scale info
        scale_text = f"Scale ~1:{scale:,}"
        draw.rectangle([(self.width - 450, 20), (self.width - 20, 80)], fill='white', outline='black', width=3)
        draw.text((self.width - 430, 35), scale_text, fill='black', font=info_font)
        
        # Add city labels for major cities
        for city in cities:
            if city.get('type') == 'major':
                # Convert lat/lon to pixel coordinates
                x, y = self._latlon_to_pixels(city['latitude'], city['longitude'], 
                                            self.center_lat, self.center_lon, 
                                            self.zoom_level, self.width, self.height)
                if 0 <= x <= self.width and 0 <= y <= self.height:
                    # Draw label with background
                    text = city['name']
                    bbox = draw.textbbox((x + 15, y), text, font=city_font)
                    draw.rectangle(bbox, fill='white', outline='white')
                    draw.text((x + 15, y), text, fill='black', font=city_font)
        
        # Add border
        draw.rectangle([(5, 5), (self.width - 5, self.height - 5)], outline='black', width=10)
        
        # Save image
        image.save(output_path)
        return output_path
    
    def _latlon_to_pixels(self, lat, lon, center_lat, center_lon, zoom, width, height):
        """Convert lat/lon to pixel coordinates."""
        # Simple mercator projection
        import math
        
        # Calculate pixel position relative to center
        n = 2.0 ** zoom
        center_x = (center_lon + 180.0) / 360.0 * n
        center_y = (1.0 - math.asinh(math.tan(math.radians(center_lat))) / math.pi) / 2.0 * n
        
        x = (lon + 180.0) / 360.0 * n
        y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
        
        # Convert to pixel coordinates
        tile_size = 256
        pixel_x = width / 2 + (x - center_x) * tile_size
        pixel_y = height / 2 + (y - center_y) * tile_size
        
        return int(pixel_x), int(pixel_y)
    
    def generate_map(self, output_path: Optional[str] = None) -> str:
        """Generate the map."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        return self.generate_map_with_staticmap(output_path)


def create_map_image(map_id: int = 1, output_filename: str = "map.png") -> str:
    """Create a static map image."""
    generator = StaticFoliumMapGenerator(map_id=map_id)
    return generator.generate_map(output_filename)