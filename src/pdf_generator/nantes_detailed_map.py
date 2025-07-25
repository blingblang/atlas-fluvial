"""Generate detailed maps for Nantes region with cities, coastline, and features."""

import os
import math
import tempfile
from typing import Tuple, Optional, List, Dict, Set
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json


class NantesDetailedMap:
    """Generate detailed maps for Nantes region with all features."""
    
    def __init__(self):
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
        
        # Cities with approximate coordinates
        self.cities = {
            # Major cities
            "Nantes": (47.2184, -1.5536, "major"),
            "Saint-Nazaire": (47.2733, -2.2134, "major"),
            
            # Coastal cities
            "Pornic": (47.1156, -2.1028, "medium"),
            "Saint-Brévin-les-Pins": (47.2472, -2.1656, "medium"),
            "La Turballe": (47.3469, -2.5072, "medium"),
            "Guérande": (47.3280, -2.4288, "medium"),
            "La Baule": (47.2869, -2.3908, "medium"),
            "Pornichet": (47.2600, -2.3400, "medium"),
            "Saint-Marc-sur-Mer": (47.2600, -2.3100, "small"),
            "Saint-Michel-Chef-Chef": (47.1819, -2.1483, "small"),
            
            # Vendée coastal
            "Saint-Gilles-Croix-de-Vie": (46.6958, -1.9414, "medium"),
            "Saint-Jean-de-Monts": (46.7933, -2.0592, "medium"),
            "Notre-Dame-de-Monts": (46.8330, -2.1290, "small"),
            "Saint-Hilaire-de-Riez": (46.7667, -1.9500, "small"),
            "Brétignolles-sur-Mer": (46.6247, -1.8614, "small"),
            "Bouin": (46.9750, -2.0000, "small"),
            
            # Loire estuary
            "Paimbœuf": (47.2867, -2.0292, "small"),
            "Corsept": (47.2781, -2.0625, "small"),
            "Frossay": (47.2450, -1.9319, "small"),
            "Le Pellerin": (47.2000, -1.7533, "small"),
            "Couëron": (47.2150, -1.7217, "medium"),
            "Indre": (47.2000, -1.6667, "small"),
            
            # Nantes periphery
            "Rezé": (47.1833, -1.5500, "medium"),
            "Vertou": (47.1689, -1.4697, "medium"),
            "Saint-Sébastien-sur-Loire": (47.2078, -1.5039, "medium"),
            "Orvault": (47.2708, -1.6228, "medium"),
            "Carquefou": (47.2975, -1.4917, "medium"),
            "La Chapelle-sur-Erdre": (47.3000, -1.5500, "medium"),
            "Sautron": (47.2608, -1.6703, "small"),
            "Basse-Goulaine": (47.2028, -1.4481, "small"),
            "Saint-Aignan-Grandlieu": (47.1267, -1.6300, "small"),
            
            # Inland Vendée
            "Challans": (46.8433, -1.8783, "medium"),
            "Machecoul": (46.9933, -1.8233, "medium"),
            "Sainte-Pazanne": (47.1033, -1.8100, "small"),
            "Legé": (46.8861, -1.5989, "small"),
            "Sainte-Hermine": (46.5558, -1.0619, "small"),
            "Bournezeau": (46.6356, -1.1753, "small"),
            "Sainte-Radégonde-des-Noyers": (46.7064, -0.9894, "small"),
            
            # Wine region
            "Vallet": (47.1614, -1.2667, "medium"),
            "Clisson": (47.0875, -1.2822, "medium"),
            "Le Loroux-Bottereau": (47.2392, -1.3489, "small"),
            "La Chapelle-Heulin": (47.1775, -1.3339, "small"),
            "Remouillé": (47.0578, -1.3836, "small"),
            "Maisdon-sur-Sèvre": (47.0961, -1.3831, "small"),
            "Aigrefeuille-sur-Maine": (46.9442, -1.3061, "small"),
            
            # North Loire
            "Nort-sur-Erdre": (47.4392, -1.4994, "small"),
            "Saint-André-des-Eaux": (47.3156, -2.3156, "small"),
            "La Montagne": (47.1872, -1.6844, "small"),
            "Barbechat": (47.2833, -1.2833, "small"),
            "Ingrandes": (47.4067, -0.9206, "small"),
            "Ponton": (47.3500, -1.8500, "small"),  # Approximate
        }
        
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
        # Go to southeast corner
        land_points.append((img_width, img_height))
        # Go to northeast corner  
        land_points.append((img_width, 0))
        # Go to top of coastline
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
        """Draw all cities on the map."""
        for city_name, (lat, lon, size) in self.cities.items():
            if bounds[1] <= lon <= bounds[3] and bounds[2] <= lat <= bounds[0]:
                x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
                
                # City dot size based on importance
                if size == "major":
                    radius = 8
                    font_size = self.city_font_size + 4
                elif size == "medium":
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
        """Generate the detailed Nantes region map."""
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
        
        img.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path


def create_map_image(latitude: float, longitude: float, 
                    output_filename: str = "map.png") -> str:
    """Create a map image from given NW coordinates."""
    generator = NantesDetailedMap()
    return generator.generate_map(latitude, longitude, output_filename)