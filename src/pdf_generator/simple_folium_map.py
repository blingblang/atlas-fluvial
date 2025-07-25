"""Generate maps using Folium - simpler version that outputs HTML."""

import folium
import json
from pathlib import Path
import tempfile
from typing import Dict, List, Optional
import webbrowser


class SimpleFoliumMapGenerator:
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
        # Approximate conversion from scale to zoom level
        scale_to_zoom = {
            1000000: 8,
            500000: 9,
            375000: 10,
            250000: 11,
            150000: 12,
            100000: 13,
            50000: 14,
            25000: 15
        }
        
        # Find closest scale
        closest_scale = min(scale_to_zoom.keys(), key=lambda x: abs(x - self.scale))
        self.zoom_level = scale_to_zoom[closest_scale]
    
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
            output_path = tempfile.mktemp(suffix='.html')
        elif not output_path.endswith('.html'):
            output_path = output_path.replace('.png', '.html')
        
        # Create folium map with a good base layer for coastal areas
        m = folium.Map(
            location=[self.center_lat, self.center_lon],
            zoom_start=self.zoom_level,
            tiles='OpenStreetMap',
            width='100%',
            height='100%'
        )
        
        # Add a satellite layer option
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satellite',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add cities
        cities = self._filter_municipalities_for_map()
        city_group = folium.FeatureGroup(name='Cities')
        
        for city in cities:
            # Determine marker style based on city type
            city_type = city.get('type', 'small')
            if city_type == 'major':
                icon = folium.Icon(color='red', icon='star')
            elif city_type == 'medium':
                icon = folium.Icon(color='blue', icon='info-sign')
            else:
                icon = folium.Icon(color='gray', icon='home')
            
            # Add city marker
            folium.Marker(
                location=[city['latitude'], city['longitude']],
                popup=f"<b>{city['name']}</b><br>Type: {city_type}<br>Lat: {city['latitude']}<br>Lon: {city['longitude']}",
                tooltip=city['name'],
                icon=icon
            ).add_to(city_group)
        
        city_group.add_to(m)
        
        # Add map info as HTML
        info_html = f'''
        <div style="position: fixed; 
                    top: 10px; left: 50%; transform: translateX(-50%);
                    background-color: rgba(255,255,255,0.9); 
                    border: 2px solid black; border-radius: 5px;
                    padding: 10px; z-index: 1000;">
            <h2 style="margin: 0;">{self.map_id}: {self.map_name}</h2>
            <p style="margin: 5px 0;">Scale: 1:{self.scale:,} | Center: {self.center_lat:.4f}°N, {self.center_lon:.4f}°W</p>
            <p style="margin: 5px 0;">Cities shown: {len(cities)}</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(info_html))
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save the map
        m.save(output_path)
        
        print(f"Map saved to: {output_path}")
        print(f"Center: {self.center_lat}°N, {self.center_lon}°W")
        print(f"Zoom level: {self.zoom_level}")
        print(f"Cities displayed: {len(cities)}")
        
        return output_path


def create_map_image(map_id: int = 1, output_filename: str = "map.html") -> str:
    """Create a map using Folium."""
    generator = SimpleFoliumMapGenerator(map_id=map_id)
    return generator.generate_map(output_filename)