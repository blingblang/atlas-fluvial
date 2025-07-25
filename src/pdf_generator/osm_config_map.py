"""Generate maps with accurate waterway geometries from OpenStreetMap."""

import os
import json
import math
import tempfile
import requests
from typing import Tuple, Optional, List, Dict
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import time


class OSMConfigMapGenerator:
    """Generate maps using configuration and real OSM waterway data."""
    
    def __init__(self, map_id: int = 1):
        self.map_id = map_id
        self.paper_size = (297, 210)  # A4 landscape in mm
        self.dpi = 300  # High quality for print
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Colors
        self.ocean_color = (135, 206, 235)  # Sky blue for ocean
        self.land_color = (255, 255, 255)  # White for land
        self.waterway_color = (0, 119, 190)  # Darker blue for rivers
        self.motorway_color = (255, 0, 0)  # Red for motorways
        self.city_color = (0, 0, 0)  # Black for cities
        
        # Font sizes
        self.title_font_size = 36
        self.city_font_size = 14
        self.waterway_font_size = 16
        self.info_font_size = 18
        
        # Load configurations and municipalities
        self.map_config = self._load_map_configuration()
        self.municipalities = self._load_municipalities()
        
        # Extract configuration values
        self.scale = self.map_config.get('scale', 375000)
        self.center_lat = self.map_config['center_latitude']
        self.center_lon = self.map_config['center_longitude']
        self.slope = self.map_config.get('slope', 0)
        self.map_name = self.map_config['name']
        
        # Target waterways
        self.target_waterways = {
            'Loire', 'Vilaine', 'Brivet', 'Canal de Nantes à Brest',
            'Erdre', 'Sèvre Nantaise', 'Don', 'Saint Eloi', 'Saint-Eloi'
        }
    
    def _load_map_configuration(self) -> Dict:
        """Load map configuration from JSON file."""
        json_path = Path(__file__).parent / "map_configurations.json"
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                maps = data.get('maps', [])
                for map_config in maps:
                    if map_config['id'] == self.map_id:
                        return map_config
                return {
                    'id': self.map_id,
                    'name': f'Map {self.map_id}',
                    'center_latitude': 47.2184,
                    'center_longitude': -1.5536,
                    'slope': 0,
                    'scale': 375000
                }
        except Exception as e:
            print(f"Error loading map_configurations.json: {e}")
            return {
                'id': self.map_id,
                'name': f'Map {self.map_id}',
                'center_latitude': 47.2184,
                'center_longitude': -1.5536,
                'slope': 0,
                'scale': 375000
            }
    
    def _load_municipalities(self) -> List[Dict]:
        """Load municipalities from JSON file."""
        json_path = Path(__file__).parent / "municipalities.json"
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('municipalities', [])
        except Exception as e:
            print(f"Error loading municipalities.json: {e}")
            return []
    
    def _filter_municipalities_for_map(self) -> List[Dict]:
        """Filter municipalities that should appear on this map."""
        return [m for m in self.municipalities if self.map_id in m.get('maps', [])]
    
    def calculate_map_bounds_from_center(self) -> Tuple[float, float, float, float]:
        """Calculate map bounds from center coordinates."""
        paper_width_m = (self.paper_size[0] / 1000) * self.scale
        paper_height_m = (self.paper_size[1] / 1000) * self.scale
        
        earth_radius = 6371000
        
        half_lat_span = (paper_height_m / 2) / earth_radius * (180 / math.pi)
        half_lon_span = (paper_width_m / 2) / (earth_radius * math.cos(math.radians(self.center_lat))) * (180 / math.pi)
        
        nw_lat = self.center_lat + half_lat_span
        se_lat = self.center_lat - half_lat_span
        nw_lon = self.center_lon - half_lon_span
        se_lon = self.center_lon + half_lon_span
        
        return nw_lat, nw_lon, se_lat, se_lon
    
    def fetch_waterways_from_osm(self, bounds: Tuple[float, float, float, float]) -> Dict[str, List]:
        """Fetch real waterway geometries from OpenStreetMap."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        
        # Expand bounds slightly to ensure we get complete waterways
        buffer = 0.1
        bbox = f"{se_lat-buffer},{nw_lon-buffer},{nw_lat+buffer},{se_lon+buffer}"
        
        # Query for waterways - temporarily just Vilaine
        query = f"""
        [out:json][timeout:30];
        (
          way["waterway"="river"]["name"~"Vilaine",i]({bbox});
          way["waterway"="canal"]["name"~"Vilaine",i]({bbox});
          relation["waterway"]["name"~"Vilaine",i]({bbox});
        );
        out geom;
        """
        
        try:
            print(f"Fetching waterways from OSM for bounds: {bbox}")
            response = requests.post(self.overpass_url, data=query, timeout=30)
            if response.status_code == 200:
                data = response.json()
                waterways = {}
                
                for element in data.get('elements', []):
                    tags = element.get('tags', {})
                    name = tags.get('name', '')
                    
                    # Since we're only querying for Vilaine, just add it
                    if name and 'geometry' in element:
                        coords = [(node['lat'], node['lon']) for node in element['geometry']]
                        if name not in waterways:
                            waterways[name] = []
                        waterways[name].extend(coords)
                
                print(f"Found {len(waterways)} waterways with geometry")
                if not waterways:
                    # Fallback for Vilaine if OSM data not available
                    print("No Vilaine data from OSM, using fallback coordinates")
                    waterways['Vilaine'] = self._get_vilaine_fallback()
                return waterways
            else:
                print(f"OSM query failed with status {response.status_code}")
                return {'Vilaine': self._get_vilaine_fallback()}
        except Exception as e:
            print(f"Error fetching OSM data: {e}")
            # Return fallback Vilaine data
            return {'Vilaine': self._get_vilaine_fallback()}
    
    def _get_vilaine_fallback(self) -> List[Tuple[float, float]]:
        """Get fallback coordinates for Vilaine river."""
        # Vilaine river approximate path from Redon area towards the ocean
        return [
            (47.65, -2.08),  # Near Redon
            (47.63, -2.10),
            (47.60, -2.13),
            (47.57, -2.15),
            (47.54, -2.17),
            (47.51, -2.20),
            (47.48, -2.23),
            (47.45, -2.26),
            (47.42, -2.29),
            (47.39, -2.32),
            (47.36, -2.35),
            (47.33, -2.38),
            (47.30, -2.41),
            (47.27, -2.44),
            (47.24, -2.47),
            (47.21, -2.50),
            (47.18, -2.53),  # Mouth at ocean
        ]
    
    def fetch_coastline_from_osm(self, bounds: Tuple[float, float, float, float]) -> List[Tuple[float, float]]:
        """Fetch coastline data from OpenStreetMap."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        
        # Query for coastline
        bbox = f"{se_lat},{nw_lon},{nw_lat},{se_lon}"
        query = f"""
        [out:json][timeout:30];
        (
          way["natural"="coastline"]({bbox});
          relation["natural"="coastline"]({bbox});
        );
        out geom;
        """
        
        try:
            response = requests.post(self.overpass_url, data=query, timeout=30)
            if response.status_code == 200:
                data = response.json()
                coastline_points = []
                
                for element in data.get('elements', []):
                    if 'geometry' in element:
                        coords = [(node['lat'], node['lon']) for node in element['geometry']]
                        coastline_points.extend(coords)
                
                # Sort points to form continuous coastline
                if coastline_points:
                    return self._sort_coastline_points(coastline_points)
                
            return self._get_default_coastline()
        except Exception as e:
            print(f"Error fetching coastline: {e}")
            return self._get_default_coastline()
    
    def _get_default_coastline(self) -> List[Tuple[float, float]]:
        """Return default coastline points."""
        return [
            (47.50, -2.55), (47.35, -2.51), (47.32, -2.45),
            (47.28, -2.39), (47.26, -2.34), (47.25, -2.25),
            (47.27, -2.21), (47.25, -2.17), (47.20, -2.15),
            (47.12, -2.10), (47.05, -2.12), (46.95, -2.15),
            (46.85, -2.18), (46.75, -2.10), (46.65, -1.95),
            (46.60, -1.85)
        ]
    
    def _sort_coastline_points(self, points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """Sort coastline points to form a continuous line."""
        if not points:
            return []
        
        sorted_points = [points[0]]
        remaining = points[1:]
        
        while remaining:
            last_point = sorted_points[-1]
            nearest_idx = min(range(len(remaining)), 
                            key=lambda i: self._distance(last_point, remaining[i]))
            sorted_points.append(remaining.pop(nearest_idx))
        
        return sorted_points
    
    def _distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """Calculate distance between two points."""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def project_coordinates(self, lat: float, lon: float, bounds: Tuple[float, float, float, float],
                          img_width: int, img_height: int) -> Tuple[int, int]:
        """Project lat/lon to pixel coordinates with rotation around map center."""
        center_lat = self.center_lat
        center_lon = self.center_lon
        
        delta_lat = lat - center_lat
        delta_lon = lon - center_lon
        
        lat_scale = img_height / (bounds[0] - bounds[2])
        lon_scale = img_width / (bounds[3] - bounds[1])
        
        x_from_center = delta_lon * lon_scale
        y_from_center = -delta_lat * lat_scale
        
        if self.slope != 0:
            angle_rad = math.radians(self.slope)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            
            x_rotated = x_from_center * cos_a - y_from_center * sin_a
            y_rotated = x_from_center * sin_a + y_from_center * cos_a
            
            x_from_center = x_rotated
            y_from_center = y_rotated
        
        x = int(img_width / 2 + x_from_center)
        y = int(img_height / 2 + y_from_center)
        
        return x, y
    
    def draw_coastline_and_ocean(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                                img_width: int, img_height: int, coastline_data: List[Tuple[float, float]]):
        """Draw coastline and fill ocean area."""
        draw.rectangle([(0, 0), (img_width, img_height)], fill=self.ocean_color)
        
        land_points = []
        for lat, lon in coastline_data:
            x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
            if 0 <= x < img_width and 0 <= y < img_height:
                land_points.append((x, y))
        
        if len(land_points) > 2:
            # Extend to edges
            edge_points = [
                (img_width * 2, img_height * 2),
                (img_width * 2, -img_height),
                (-img_width, -img_height),
                (-img_width, img_height * 2)
            ]
            for edge_point in edge_points:
                land_points.append(edge_point)
            
            draw.polygon(land_points, fill=self.land_color, outline=(100, 100, 100), width=3)
        
        try:
            font = ImageFont.truetype("arial.ttf", self.info_font_size)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, img_height // 2), "ATLANTIC\nOCEAN", fill=(0, 50, 150), font=font)
    
    def draw_waterways(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                      img_width: int, img_height: int, waterway_data: Dict[str, List]):
        """Draw waterways with accurate geometries."""
        try:
            font = ImageFont.truetype("arial.ttf", self.waterway_font_size)
        except:
            font = ImageFont.load_default()
        
        # Define waterway widths
        waterway_widths = {
            'Loire': 20,
            'Vilaine': 15,
            'Erdre': 12,
            'Sèvre Nantaise': 10,
            'Don': 10,
            'Brivet': 10,
            'Canal de Nantes à Brest': 8,
            'Saint Eloi': 8,
            'Saint-Eloi': 8
        }
        
        # Draw each waterway
        for name, coordinates in waterway_data.items():
            if not coordinates:
                continue
            
            # Convert coordinates to pixel points
            points = []
            for lat, lon in coordinates:
                x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
                points.append((x, y))
            
            # Filter out points outside the image
            valid_points = [(x, y) for x, y in points 
                          if -100 <= x <= img_width + 100 and -100 <= y <= img_height + 100]
            
            if len(valid_points) > 1:
                # Determine width
                width = waterway_widths.get(name, 10)
                
                # Draw the waterway as a series of connected lines
                for i in range(len(valid_points) - 1):
                    draw.line([valid_points[i], valid_points[i+1]], 
                            fill=self.waterway_color, width=width)
                
                # Add label at a reasonable position
                if len(valid_points) > 5:
                    label_idx = len(valid_points) // 2
                    label_x, label_y = valid_points[label_idx]
                    if 0 <= label_x <= img_width and 0 <= label_y <= img_height:
                        # Draw text with white background for readability
                        text_bbox = draw.textbbox((label_x, label_y), name, font=font)
                        draw.rectangle(text_bbox, fill='white', outline='white')
                        draw.text((label_x, label_y), name, fill=self.waterway_color, font=font)
    
    def draw_motorways_from_osm(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                               img_width: int, img_height: int):
        """Fetch and draw motorways from OSM."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        bbox = f"{se_lat},{nw_lon},{nw_lat},{se_lon}"
        
        query = f"""
        [out:json][timeout:30];
        (
          way["highway"="motorway"]["ref"="N165"]({bbox});
          way["highway"="trunk"]["ref"="N165"]({bbox});
        );
        out geom;
        """
        
        try:
            response = requests.post(self.overpass_url, data=query, timeout=30)
            if response.status_code == 200:
                data = response.json()
                
                for element in data.get('elements', []):
                    if 'geometry' in element:
                        points = []
                        for node in element['geometry']:
                            x, y = self.project_coordinates(node['lat'], node['lon'], 
                                                          bounds, img_width, img_height)
                            points.append((x, y))
                        
                        # Draw motorway
                        if len(points) > 1:
                            for i in range(len(points) - 1):
                                draw.line([points[i], points[i+1]], fill=self.motorway_color, width=8)
                                draw.line([points[i], points[i+1]], fill='white', width=4)
                                draw.line([points[i], points[i+1]], fill=self.motorway_color, width=2)
                            
                            # Add shield
                            if len(points) > 5:
                                shield_x, shield_y = points[len(points)//2]
                                if 0 <= shield_x <= img_width and 0 <= shield_y <= img_height:
                                    draw.rectangle([shield_x - 25, shield_y - 18, shield_x + 25, shield_y + 18], 
                                                 fill='white', outline=self.motorway_color, width=3)
                                    try:
                                        font = ImageFont.truetype("arial.ttf", 16)
                                    except:
                                        font = ImageFont.load_default()
                                    draw.text((shield_x - 18, shield_y - 12), "N165", fill=self.motorway_color, font=font)
        except Exception as e:
            print(f"Error fetching motorways: {e}")
    
    def draw_cities(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                   img_width: int, img_height: int):
        """Draw cities from JSON data on the map."""
        cities_to_draw = self._filter_municipalities_for_map()
        
        for city in cities_to_draw:
            lat = city['latitude']
            lon = city['longitude']
            
            x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
            
            if 0 <= x <= img_width and 0 <= y <= img_height:
                city_type = city.get('type', 'small')
                city_name = city['name']
                
                radius = {'major': 8, 'medium': 6, 'small': 4}.get(city_type, 4)
                font_size = {'major': self.city_font_size + 4, 'medium': self.city_font_size, 
                           'small': self.city_font_size - 2}.get(city_type, self.city_font_size)
                
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=self.city_color, outline='white', width=1)
                
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                draw.text((x + radius + 3, y - font_size // 2), city_name, fill=self.city_color, font=font)
    
    def generate_map(self, output_path: Optional[str] = None) -> str:
        """Generate the map using configuration and OSM data."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        bounds = self.calculate_map_bounds_from_center()
        
        # Fetch real data from OSM
        print("Fetching waterway data from OpenStreetMap...")
        waterway_data = self.fetch_waterways_from_osm(bounds)
        
        print("Fetching coastline data from OpenStreetMap...")
        coastline_data = self.fetch_coastline_from_osm(bounds)
        
        target_width = int(self.paper_size[0] * self.dpi / 25.4)
        target_height = int(self.paper_size[1] * self.dpi / 25.4)
        
        img = Image.new('RGB', (target_width, target_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw features
        self.draw_coastline_and_ocean(draw, bounds, target_width, target_height, coastline_data)
        self.draw_waterways(draw, bounds, target_width, target_height, waterway_data)
        self.draw_motorways_from_osm(draw, bounds, target_width, target_height)
        self.draw_cities(draw, bounds, target_width, target_height)
        
        # Draw border
        draw.rectangle([(10, 10), (target_width - 10, target_height - 10)],
                      outline='black', width=10)
        
        # Add title and info
        try:
            title_font = ImageFont.truetype("arial.ttf", self.title_font_size)
            info_font = ImageFont.truetype("arial.ttf", self.info_font_size)
        except:
            title_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
        
        draw.text((30, 30), f"{self.map_id}: {self.map_name}", fill='black', font=title_font)
        draw.text((target_width - 300, 30), f"Scale 1:{self.scale:,}", fill='black', font=info_font)
        
        cities_count = len(self._filter_municipalities_for_map())
        draw.text((30, target_height - 60), 
                 f"Center: {self.center_lat:.4f}°N, {self.center_lon:.4f}°E | {cities_count} municipalities | OSM data", 
                 fill='black', font=info_font)
        
        img.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path


def create_map_image(map_id: int = 1, output_filename: str = "map.png") -> str:
    """Create a map image for the specified map ID with real OSM data."""
    generator = OSMConfigMapGenerator(map_id=map_id)
    return generator.generate_map(output_filename)