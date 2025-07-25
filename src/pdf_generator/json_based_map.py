"""Generate maps using municipality data from JSON file."""

import os
import json
import math
import tempfile
from typing import Tuple, Optional, List, Dict, Set
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


class JSONBasedMapGenerator:
    """Generate maps using municipality data from JSON file."""
    
    def __init__(self, map_number: int = 1):
        self.map_number = map_number
        self.scale = 375000  # 1:375,000 scale
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
        
        # Load municipalities from JSON
        self.municipalities = self._load_municipalities()
        
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
        filtered = []
        for municipality in self.municipalities:
            if self.map_number in municipality.get('maps', []):
                filtered.append(municipality)
        return filtered
    
    def calculate_map_bounds(self, nw_lat: float, nw_lon: float) -> Tuple[float, float, float, float]:
        """Calculate SE corner based on NW corner and A4 paper size at given scale."""
        paper_width_m = (self.paper_size[0] / 1000) * self.scale
        paper_height_m = (self.paper_size[1] / 1000) * self.scale
        
        earth_radius = 6371000
        
        lat_change = (paper_height_m / earth_radius) * (180 / math.pi)
        se_lat = nw_lat - lat_change
        
        avg_lat = (nw_lat + se_lat) / 2
        lon_change = (paper_width_m / (earth_radius * math.cos(math.radians(avg_lat)))) * (180 / math.pi)
        se_lon = nw_lon + lon_change
        
        return nw_lat, nw_lon, se_lat, se_lon
    
    def project_coordinates(self, lat: float, lon: float, bounds: Tuple[float, float, float, float],
                          img_width: int, img_height: int) -> Tuple[int, int]:
        """Project lat/lon to pixel coordinates."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        
        x = int((lon - nw_lon) / (se_lon - nw_lon) * img_width)
        y = int((nw_lat - lat) / (nw_lat - se_lat) * img_height)
        
        x = max(0, min(img_width - 1, x))
        y = max(0, min(img_height - 1, y))
        
        return x, y
    
    def draw_coastline_and_ocean(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                                img_width: int, img_height: int):
        """Draw coastline and fill ocean area."""
        # First, fill entire image with ocean color
        draw.rectangle([(0, 0), (img_width, img_height)], fill=self.ocean_color)
        
        # Create land polygon
        land_points = []
        
        # Add coastline points
        for lat, lon in self.coastline:
            x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
            land_points.append((x, y))
        
        # Complete the land polygon by going to map edges
        land_points.append((img_width, img_height))
        land_points.append((img_width, 0))
        land_points.append((land_points[0][0], 0))
        
        # Draw land area
        if len(land_points) > 2:
            draw.polygon(land_points, fill=self.land_color, outline=(100, 100, 100), width=3)
        
        # Add coastline label
        try:
            font = ImageFont.truetype("arial.ttf", self.info_font_size)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, img_height // 2), "ATLANTIC\nOCEAN", fill=(0, 50, 150), font=font)
    
    def draw_waterways(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                      img_width: int, img_height: int):
        """Draw navigable waterways."""
        try:
            font = ImageFont.truetype("arial.ttf", self.waterway_font_size)
        except:
            font = ImageFont.load_default()
        
        # Loire
        loire_points = []
        for i in range(15):
            lon = -0.8 - (i * 0.1)
            lat = 47.2184 + math.sin(i * 0.3) * 0.02
            if bounds[1] <= lon <= bounds[3]:
                x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
                loire_points.append((x, y))
        
        for i in range(len(loire_points) - 1):
            draw.line([loire_points[i], loire_points[i+1]], fill=self.waterway_color, width=20)
        
        if len(loire_points) > 5:
            draw.text((loire_points[5][0], loire_points[5][1] + 25), "Loire", fill=self.waterway_color, font=font)
        
        # Erdre
        erdre_start = self.project_coordinates(47.35, -1.55, bounds, img_width, img_height)
        erdre_end = self.project_coordinates(47.2136, -1.5522, bounds, img_width, img_height)
        draw.line([erdre_start, erdre_end], fill=self.waterway_color, width=12)
        draw.text((erdre_start[0] + 10, erdre_start[1] + 20), "Erdre", fill=self.waterway_color, font=font)
        
        # Sèvre Nantaise
        sevre_start = self.project_coordinates(47.0, -1.2, bounds, img_width, img_height)
        sevre_end = self.project_coordinates(47.19, -1.54, bounds, img_width, img_height)
        draw.line([sevre_start, sevre_end], fill=self.waterway_color, width=10)
        draw.text((sevre_start[0] - 80, sevre_start[1] - 20), "Sèvre Nantaise", fill=self.waterway_color, font=font)
        
        # Vilaine
        vilaine_points = []
        for i in range(8):
            lon = -1.8 - (i * 0.1)
            lat = 47.5 - (i * 0.02)
            if bounds[1] <= lon <= bounds[3]:
                x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
                vilaine_points.append((x, y))
        
        for i in range(len(vilaine_points) - 1):
            draw.line([vilaine_points[i], vilaine_points[i+1]], fill=self.waterway_color, width=15)
        
        if len(vilaine_points) > 2:
            draw.text((vilaine_points[2][0], vilaine_points[2][1] - 25), "Vilaine", fill=self.waterway_color, font=font)
        
        # Don
        don_start = self.project_coordinates(47.55, -1.85, bounds, img_width, img_height)
        don_end = self.project_coordinates(47.48, -2.0, bounds, img_width, img_height)
        draw.line([don_start, don_end], fill=self.waterway_color, width=10)
        draw.text((don_start[0] - 30, don_start[1] - 20), "Don", fill=self.waterway_color, font=font)
        
        # Brivet
        brivet_start = self.project_coordinates(47.35, -2.15, bounds, img_width, img_height)
        brivet_end = self.project_coordinates(47.28, -2.20, bounds, img_width, img_height)
        draw.line([brivet_start, brivet_end], fill=self.waterway_color, width=10)
        draw.text((brivet_start[0] + 10, brivet_start[1] + 10), "Brivet", fill=self.waterway_color, font=font)
        
        # Canal de Nantes à Brest
        canal_start = self.project_coordinates(47.22, -1.58, bounds, img_width, img_height)
        canal_mid = self.project_coordinates(47.35, -1.75, bounds, img_width, img_height)
        canal_end = self.project_coordinates(47.5, -2.0, bounds, img_width, img_height)
        
        draw.line([canal_start, canal_mid], fill=self.waterway_color, width=8)
        draw.line([canal_mid, canal_end], fill=self.waterway_color, width=8)
        draw.text((canal_mid[0] - 50, canal_mid[1] - 20), "Canal de Nantes à Brest", fill=self.waterway_color, font=font)
        
        # Saint Eloi
        saint_eloi_start = self.project_coordinates(47.25, -1.48, bounds, img_width, img_height)
        saint_eloi_end = self.project_coordinates(47.20, -1.52, bounds, img_width, img_height)
        draw.line([saint_eloi_start, saint_eloi_end], fill=self.waterway_color, width=8)
        draw.text((saint_eloi_start[0] + 10, saint_eloi_start[1] - 20), "Saint Eloi", fill=self.waterway_color, font=font)
    
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
        # Get filtered municipalities for this map
        cities_to_draw = self._filter_municipalities_for_map()
        
        print(f"Drawing {len(cities_to_draw)} cities on Map {self.map_number}")
        
        for city in cities_to_draw:
            lat = city['latitude']
            lon = city['longitude']
            
            # Check if city is within map bounds
            if bounds[1] <= lon <= bounds[3] and bounds[2] <= lat <= bounds[0]:
                x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
                
                city_type = city.get('type', 'small')
                city_name = city['name']
                
                # City dot size based on importance
                if city_type == "major":
                    radius = 8
                    font_size = self.city_font_size + 4
                elif city_type == "medium":
                    radius = 6
                    font_size = self.city_font_size
                else:
                    radius = 4
                    font_size = self.city_font_size - 2
                
                # Draw city dot
                draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                           fill=self.city_color, outline='white', width=1)
                
                # Draw city name
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
                
                # Offset text to avoid overlapping with dot
                text_x = x + radius + 3
                text_y = y - font_size // 2
                
                draw.text((text_x, text_y), city_name, fill=self.city_color, font=font)
    
    def generate_map(self, nw_lat: float, nw_lon: float, 
                    output_path: Optional[str] = None) -> str:
        """Generate the map from JSON data."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        bounds = self.calculate_map_bounds(nw_lat, nw_lon)
        
        target_width = int(self.paper_size[0] * self.dpi / 25.4)
        target_height = int(self.paper_size[1] * self.dpi / 25.4)
        
        img = Image.new('RGB', (target_width, target_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw features in order
        self.draw_coastline_and_ocean(draw, bounds, target_width, target_height)
        self.draw_waterways(draw, bounds, target_width, target_height)
        self.draw_motorway(draw, bounds, target_width, target_height)
        self.draw_cities(draw, bounds, target_width, target_height)
        
        # Draw border
        draw.rectangle([(10, 10), (target_width - 10, target_height - 10)],
                      outline='black', width=10)
        
        # Add title and scale
        try:
            title_font = ImageFont.truetype("arial.ttf", self.title_font_size)
            info_font = ImageFont.truetype("arial.ttf", self.info_font_size)
        except:
            title_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
        
        draw.text((target_width - 300, 30), "Scale 1:375,000", fill='black', font=info_font)
        
        # Add map statistics
        cities_count = len(self._filter_municipalities_for_map())
        draw.text((30, target_height - 60), 
                 f"Map {self.map_number}: {cities_count} municipalities shown", 
                 fill='black', font=info_font)
        
        img.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path


def create_map_image(latitude: float, longitude: float, 
                    output_filename: str = "map.png", map_number: int = 1) -> str:
    """Create a map image from given NW coordinates."""
    generator = JSONBasedMapGenerator(map_number=map_number)
    return generator.generate_map(latitude, longitude, output_filename)