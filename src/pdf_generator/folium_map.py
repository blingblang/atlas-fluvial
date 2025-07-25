"""Generate maps using Folium for accurate real-world representation."""

import folium
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import tempfile
from typing import Dict, List, Optional
from PIL import Image
import io


class FoliumMapGenerator:
    """Generate maps using Folium with real map tiles."""
    
    def __init__(self, map_id: int = 1):
        self.map_id = map_id
        self.map_config = self._load_map_configuration()
        self.municipalities = self._load_municipalities()
        
        # Extract configuration
        self.center_lat = self.map_config['center_latitude']
        self.center_lon = self.map_config['center_longitude']
        self.scale = self.map_config.get('scale', 375000)
        self.map_name = self.map_config['name']
        
        # Calculate zoom level from scale
        # Scale 1:375,000 is approximately zoom level 10
        # Scale 1:150,000 is approximately zoom level 11
        # Scale 1:100,000 is approximately zoom level 12
        if self.scale >= 300000:
            self.zoom_level = 10
        elif self.scale >= 200000:
            self.zoom_level = 11
        elif self.scale >= 100000:
            self.zoom_level = 12
        else:
            self.zoom_level = 13
    
    def _load_map_configuration(self) -> Dict:
        """Load map configuration from JSON file."""
        json_path = Path(__file__).parent / "map_configurations.json"
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            maps = data.get('maps', [])
            for map_config in maps:
                if map_config['id'] == self.map_id:
                    return map_config
            
            # Default if not found
            return {
                'id': self.map_id,
                'name': f'Map {self.map_id}',
                'center_latitude': 47.2184,
                'center_longitude': -1.5536,
                'scale': 375000
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
    
    def generate_map(self, output_path: Optional[str] = None) -> str:
        """Generate the map using Folium."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        # Create folium map
        m = folium.Map(
            location=[self.center_lat, self.center_lon],
            zoom_start=self.zoom_level,
            tiles='OpenStreetMap',
            prefer_canvas=True
        )
        
        # Add cities
        cities = self._filter_municipalities_for_map()
        for city in cities:
            # Determine marker size and color based on city type
            city_type = city.get('type', 'small')
            if city_type == 'major':
                radius = 8
                color = 'red'
                weight = 3
            elif city_type == 'medium':
                radius = 6
                color = 'blue'
                weight = 2
            else:
                radius = 4
                color = 'gray'
                weight = 1
            
            # Add city marker
            folium.CircleMarker(
                location=[city['latitude'], city['longitude']],
                radius=radius,
                popup=city['name'],
                tooltip=city['name'],
                color=color,
                weight=weight,
                fillColor=color,
                fillOpacity=0.8
            ).add_to(m)
            
            # Add city label for major cities
            if city_type == 'major':
                folium.Marker(
                    location=[city['latitude'], city['longitude']],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 14pt; font-weight: bold; color: black; text-shadow: 1px 1px 1px white;">{city["name"]}</div>',
                        icon_size=(100, 20),
                        icon_anchor=(0, 0)
                    )
                ).add_to(m)
        
        # Add title
        title_html = f'''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 400px; height: 50px; 
                    background-color: white; border: 2px solid black;
                    z-index: 9999; font-size: 20px; font-weight: bold;
                    text-align: center; padding: 10px;">
            {self.map_id}: {self.map_name}
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Add scale info
        scale_html = f'''
        <div style="position: fixed; 
                    top: 10px; right: 50px; width: 200px; height: 30px; 
                    background-color: white; border: 2px solid black;
                    z-index: 9999; font-size: 16px;
                    text-align: center; padding: 5px;">
            Scale 1:{self.scale:,}
        </div>
        '''
        m.get_root().html.add_child(folium.Element(scale_html))
        
        # Save to HTML first
        html_path = tempfile.mktemp(suffix='.html')
        m.save(html_path)
        
        # Convert HTML to PNG using selenium
        self._html_to_png(html_path, output_path)
        
        return output_path
    
    def _html_to_png(self, html_path: str, png_path: str):
        """Convert HTML map to PNG using selenium."""
        # Setup chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=3508,2480")  # A4 at 300 DPI
        
        try:
            # Use selenium to capture screenshot
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f"file:///{html_path}")
            time.sleep(3)  # Wait for map to load
            
            # Take screenshot
            screenshot = driver.get_screenshot_as_png()
            driver.quit()
            
            # Save screenshot
            Image.open(io.BytesIO(screenshot)).save(png_path)
            
        except Exception as e:
            print(f"Error converting to PNG with selenium: {e}")
            print("Falling back to simple HTML output")
            # If selenium fails, just copy the HTML
            import shutil
            shutil.copy(html_path, png_path.replace('.png', '.html'))


def create_map_image(map_id: int = 1, output_filename: str = "map.png") -> str:
    """Create a map image using Folium."""
    generator = FoliumMapGenerator(map_id=map_id)
    return generator.generate_map(output_filename)