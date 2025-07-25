"""Generate maps using configuration from JSON file."""

import os
import json
import math
import tempfile
from typing import Tuple, Optional, List, Dict
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import numpy as np


class ConfigBasedMapGenerator:
    """Generate maps using configuration and municipality data from JSON files."""
    
    def __init__(self, map_id: int = 1):
        self.map_id = map_id
        self.paper_size = (297, 210)  # A4 landscape in mm
        self.dpi = 300  # High quality for print
        
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
        
        # Coastline points (simplified)
        self.coastline = [
            (47.50, -2.55),  # North of La Turballe
            (47.35, -2.51),  # La Turballe
            (47.32, -2.45),  # Guérande area
            (47.28, -2.39),  # La Baule
            (47.26, -2.34),  # Pornichet
            (47.25, -2.25),  # Saint-Marc
            (47.27, -2.21),  # Saint-Nazaire
            (47.25, -2.17),  # Saint-Brévin
            (47.20, -2.15),  # River mouth
            (47.12, -2.10),  # Pornic
            (47.05, -2.12),  # South of Pornic
            (46.95, -2.15),  # Bouin area
            (46.85, -2.18),  # Notre-Dame-de-Monts
            (46.75, -2.10),  # Saint-Jean-de-Monts
            (46.65, -1.95),  # Saint-Gilles
            (46.60, -1.85),  # Brétignolles
        ]
    
    def _load_map_configuration(self) -> Dict:
        """Load map configuration from JSON file."""
        json_path = Path(__file__).parent / "map_configurations.json"
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                maps = data.get('maps', [])
                # Find the configuration for this map ID
                for map_config in maps:
                    if map_config['id'] == self.map_id:
                        return map_config
                # Default if not found
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
        # Convert paper dimensions to meters
        paper_width_m = (self.paper_size[0] / 1000) * self.scale
        paper_height_m = (self.paper_size[1] / 1000) * self.scale
        
        # Earth's radius in meters
        earth_radius = 6371000
        
        # Calculate half spans
        half_lat_span = (paper_height_m / 2) / earth_radius * (180 / math.pi)
        half_lon_span = (paper_width_m / 2) / (earth_radius * math.cos(math.radians(self.center_lat))) * (180 / math.pi)
        
        # Calculate bounds before rotation
        nw_lat = self.center_lat + half_lat_span
        se_lat = self.center_lat - half_lat_span
        nw_lon = self.center_lon - half_lon_span
        se_lon = self.center_lon + half_lon_span
        
        return nw_lat, nw_lon, se_lat, se_lon
    
    def rotate_point(self, x: float, y: float, cx: float, cy: float, angle_deg: float) -> Tuple[float, float]:
        """Rotate a point around a center by given angle in degrees."""
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Translate to origin
        x -= cx
        y -= cy
        
        # Rotate
        x_new = x * cos_a - y * sin_a
        y_new = x * sin_a + y * cos_a
        
        # Translate back
        return x_new + cx, y_new + cy
    
    def project_coordinates(self, lat: float, lon: float, bounds: Tuple[float, float, float, float],
                          img_width: int, img_height: int) -> Tuple[int, int]:
        """Project lat/lon to pixel coordinates with rotation around map center."""
        # First, convert lat/lon to normalized coordinates relative to map center
        center_lat = self.center_lat
        center_lon = self.center_lon
        
        # Calculate position relative to center in degrees
        delta_lat = lat - center_lat
        delta_lon = lon - center_lon
        
        # Convert to pixel distances from center
        # Account for latitude in longitude scaling
        lat_scale = img_height / (bounds[0] - bounds[2])
        lon_scale = img_width / (bounds[3] - bounds[1])
        
        x_from_center = delta_lon * lon_scale
        y_from_center = -delta_lat * lat_scale  # Negative because lat increases upward
        
        # Apply rotation around center if slope is not 0
        if self.slope != 0:
            angle_rad = math.radians(self.slope)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            
            # Rotate coordinates
            x_rotated = x_from_center * cos_a - y_from_center * sin_a
            y_rotated = x_from_center * sin_a + y_from_center * cos_a
            
            x_from_center = x_rotated
            y_from_center = y_rotated
        
        # Convert back to pixel coordinates
        x = int(img_width / 2 + x_from_center)
        y = int(img_height / 2 + y_from_center)
        
        # Clamp to image bounds
        x = max(0, min(img_width - 1, x))
        y = max(0, min(img_height - 1, y))
        
        return x, y
    
    def draw_coastline_and_ocean(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                                img_width: int, img_height: int):
        """Draw coastline and fill ocean area."""
        # Fill entire image with ocean color
        draw.rectangle([(0, 0), (img_width, img_height)], fill=self.ocean_color)
        
        # Create land polygon
        land_points = []
        
        # Add coastline points
        for lat, lon in self.coastline:
            x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
            land_points.append((x, y))
        
        # Complete the land polygon by extending to map edges
        # For rotated maps, we need to trace along the rotated coastline to the edges
        if len(land_points) > 0:
            # Find the extreme points that would extend to edges when rotated
            last_point = land_points[-1]
            first_point = land_points[0]
            
            # Add corner points to complete the polygon
            # This creates a land mass that extends beyond the visible area
            edge_points = [
                (img_width * 2, img_height * 2),
                (img_width * 2, -img_height),
                (-img_width, -img_height),
                (-img_width, img_height * 2)
            ]
            
            # Add edge points that are on the land side of the coastline
            for edge_point in edge_points:
                land_points.append(edge_point)
        
        # Draw land area
        if len(land_points) > 2:
            draw.polygon(land_points, fill=self.land_color, outline=(100, 100, 100), width=3)
        
        # Add ocean label
        try:
            font = ImageFont.truetype("arial.ttf", self.info_font_size)
        except:
            font = ImageFont.load_default()
        
        # Add ocean label (rotation handled by rotation of entire map if needed)
        draw.text((50, img_height // 2), "ATLANTIC\nOCEAN", fill=(0, 50, 150), font=font)
    
    def draw_waterways(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                      img_width: int, img_height: int):
        """Draw navigable waterways."""
        try:
            font = ImageFont.truetype("arial.ttf", self.waterway_font_size)
        except:
            font = ImageFont.load_default()
        
        # Define waterway paths
        waterways = [
            {
                'name': 'Loire',
                'points': [(47.2184 + math.sin(i * 0.3) * 0.02, -0.8 - (i * 0.1)) for i in range(15)],
                'width': 20
            },
            {
                'name': 'Erdre',
                'points': [(47.35, -1.55), (47.2136, -1.5522)],
                'width': 12
            },
            {
                'name': 'Sèvre Nantaise',
                'points': [(47.0, -1.2), (47.19, -1.54)],
                'width': 10
            },
            {
                'name': 'Vilaine',
                'points': [(47.5 - (i * 0.02), -1.8 - (i * 0.1)) for i in range(8)],
                'width': 15
            },
            {
                'name': 'Don',
                'points': [(47.55, -1.85), (47.48, -2.0)],
                'width': 10
            },
            {
                'name': 'Brivet',
                'points': [(47.35, -2.15), (47.28, -2.20)],
                'width': 10
            },
            {
                'name': 'Canal de Nantes à Brest',
                'points': [(47.22, -1.58), (47.35, -1.75), (47.5, -2.0)],
                'width': 8
            },
            {
                'name': 'Saint Eloi',
                'points': [(47.25, -1.48), (47.20, -1.52)],
                'width': 8
            }
        ]
        
        # Draw each waterway
        for waterway in waterways:
            points = []
            for lat, lon in waterway['points']:
                if bounds[1] <= lon <= bounds[3] and bounds[2] <= lat <= bounds[0]:
                    x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
                    points.append((x, y))
            
            # Draw the waterway
            if len(points) > 1:
                for i in range(len(points) - 1):
                    draw.line([points[i], points[i+1]], fill=self.waterway_color, width=waterway['width'])
                
                # Add label
                if len(points) > 0:
                    label_idx = len(points) // 2
                    draw.text((points[label_idx][0], points[label_idx][1] + 20), 
                             waterway['name'], fill=self.waterway_color, font=font)
    
    def draw_motorway(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                     img_width: int, img_height: int):
        """Draw N165 motorway."""
        n165_points = []
        start_lat, start_lon = 47.15, -1.60
        end_lat, end_lon = 47.65, -2.75
        
        for i in range(15):
            t = i / 14.0
            lat = start_lat + (end_lat - start_lat) * t
            lon = start_lon + (end_lon - start_lon) * t + math.sin(t * 3) * 0.05
            if bounds[1] <= lon <= bounds[3] and bounds[2] <= lat <= bounds[0]:
                x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
                n165_points.append((x, y))
        
        # Draw motorway
        for i in range(len(n165_points) - 1):
            draw.line([n165_points[i], n165_points[i+1]], fill=self.motorway_color, width=8)
            draw.line([n165_points[i], n165_points[i+1]], fill='white', width=4)
            draw.line([n165_points[i], n165_points[i+1]], fill=self.motorway_color, width=2)
        
        # Add motorway label
        if len(n165_points) > 5:
            shield_x, shield_y = n165_points[5]
            draw.rectangle([shield_x - 25, shield_y - 18, shield_x + 25, shield_y + 18], 
                         fill='white', outline=self.motorway_color, width=3)
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            draw.text((shield_x - 18, shield_y - 12), "N165", fill=self.motorway_color, font=font)
    
    def draw_cities(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                   img_width: int, img_height: int):
        """Draw cities from JSON data on the map."""
        cities_to_draw = self._filter_municipalities_for_map()
        
        for city in cities_to_draw:
            lat = city['latitude']
            lon = city['longitude']
            
            if bounds[1] <= lon <= bounds[3] and bounds[2] <= lat <= bounds[0]:
                x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
                
                city_type = city.get('type', 'small')
                city_name = city['name']
                
                # City dot size
                radius = {'major': 8, 'medium': 6, 'small': 4}.get(city_type, 4)
                font_size = {'major': self.city_font_size + 4, 'medium': self.city_font_size, 
                           'small': self.city_font_size - 2}.get(city_type, self.city_font_size)
                
                # Draw city
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=self.city_color, outline='white', width=1)
                
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                draw.text((x + radius + 3, y - font_size // 2), city_name, fill=self.city_color, font=font)
    
    def generate_map(self, output_path: Optional[str] = None) -> str:
        """Generate the map using configuration."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        bounds = self.calculate_map_bounds_from_center()
        
        target_width = int(self.paper_size[0] * self.dpi / 25.4)
        target_height = int(self.paper_size[1] * self.dpi / 25.4)
        
        img = Image.new('RGB', (target_width, target_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw features
        self.draw_coastline_and_ocean(draw, bounds, target_width, target_height)
        self.draw_waterways(draw, bounds, target_width, target_height)
        self.draw_motorway(draw, bounds, target_width, target_height)
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
        
        # Title
        draw.text((30, 30), f"{self.map_id}: {self.map_name}", fill='black', font=title_font)
        
        # Scale and info
        draw.text((target_width - 300, 30), f"Scale 1:{self.scale:,}", fill='black', font=info_font)
        
        # Map info
        cities_count = len(self._filter_municipalities_for_map())
        draw.text((30, target_height - 60), 
                 f"Center: {self.center_lat:.4f}°N, {self.center_lon:.4f}°E | Slope: {self.slope}° | {cities_count} municipalities", 
                 fill='black', font=info_font)
        
        # Save
        img.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path


def create_map_image(map_id: int = 1, output_filename: str = "map.png") -> str:
    """Create a map image for the specified map ID."""
    generator = ConfigBasedMapGenerator(map_id=map_id)
    return generator.generate_map(output_filename)