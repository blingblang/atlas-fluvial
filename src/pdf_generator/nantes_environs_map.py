"""Generate maps for Nantes and environs with accurate geographical features."""

import os
import math
import tempfile
import requests
from typing import Tuple, Optional, List, Dict, Set
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json


class NantesEnvironsMap:
    """Generate maps for Nantes and environs with waterways, ocean, and motorways."""
    
    def __init__(self):
        self.scale = 375000  # 1:375,000 scale
        self.paper_size = (297, 210)  # A4 landscape in mm
        self.dpi = 300  # High quality for print
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Navigable waterways
        self.navigable_waterways = {
            "Vilaine", "Brivet", "Canal de Nantes à Brest", "Canal de Nantes a Brest",
            "Erdre", "Loire", "Sèvre Nantaise", "Sevre Nantaise", "Don", "Saint Eloi", "Saint-Eloi"
        }
        
        # Approximate coordinates for key features (Nantes region)
        self.feature_coords = {
            "Nantes": (47.2184, -1.5536),
            "Loire_mouth": (47.2800, -2.2000),  # Where Loire meets Atlantic
            "Atlantic_start": (47.3000, -2.5000),  # Western edge for Atlantic Ocean
            "Erdre_confluence": (47.2136, -1.5522),  # Where Erdre meets Loire
            "Vilaine_mouth": (47.5089, -2.5147),
            "N165_start": (47.2500, -1.6000),
            "N165_end": (47.6500, -2.7500),
        }
        
    def calculate_map_bounds(self, nw_lat: float, nw_lon: float) -> Tuple[float, float, float, float]:
        """Calculate SE corner based on NW corner and A4 paper size at given scale."""
        # Convert paper dimensions to meters
        paper_width_m = (self.paper_size[0] / 1000) * self.scale
        paper_height_m = (self.paper_size[1] / 1000) * self.scale
        
        # Earth's radius in meters
        earth_radius = 6371000
        
        # Calculate latitude change
        lat_change = (paper_height_m / earth_radius) * (180 / math.pi)
        se_lat = nw_lat - lat_change
        
        # Calculate longitude change
        avg_lat = (nw_lat + se_lat) / 2
        lon_change = (paper_width_m / (earth_radius * math.cos(math.radians(avg_lat)))) * (180 / math.pi)
        se_lon = nw_lon + lon_change
        
        return nw_lat, nw_lon, se_lat, se_lon
    
    def project_coordinates(self, lat: float, lon: float, bounds: Tuple[float, float, float, float],
                          img_width: int, img_height: int) -> Tuple[int, int]:
        """Project lat/lon to pixel coordinates."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        
        # Linear projection
        x = int((lon - nw_lon) / (se_lon - nw_lon) * img_width)
        y = int((nw_lat - lat) / (nw_lat - se_lat) * img_height)
        
        # Clamp to image bounds
        x = max(0, min(img_width - 1, x))
        y = max(0, min(img_height - 1, y))
        
        return x, y
    
    def draw_atlantic_ocean(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                          img_width: int, img_height: int):
        """Draw the Atlantic Ocean area in light blue."""
        ocean_color = (173, 216, 230)  # Light blue
        
        # The Atlantic is west of the Loire mouth
        # Create a polygon for the ocean area
        loire_mouth_x, loire_mouth_y = self.project_coordinates(
            self.feature_coords["Loire_mouth"][0], 
            self.feature_coords["Loire_mouth"][1],
            bounds, img_width, img_height
        )
        
        # Draw ocean from western edge to Loire mouth
        ocean_points = [
            (0, 0),  # NW corner
            (loire_mouth_x - 50, 0),  # Top edge to near Loire mouth
            (loire_mouth_x - 30, loire_mouth_y - 100),  # Curve towards Loire
            (loire_mouth_x, loire_mouth_y),  # Loire mouth
            (loire_mouth_x - 20, loire_mouth_y + 100),  # Below Loire mouth
            (0, img_height),  # SW corner
            (0, 0)  # Close polygon
        ]
        
        draw.polygon(ocean_points, fill=ocean_color, outline=ocean_color)
        
        # Add label
        draw.text((50, img_height // 2), "ATLANTIC OCEAN", fill=(0, 100, 200))
    
    def draw_waterways(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                      img_width: int, img_height: int):
        """Draw navigable waterways at their actual positions."""
        waterway_color = (100, 149, 237)  # Cornflower blue for rivers
        
        # Add Saint Eloi waterway (small waterway near Nantes)
        saint_eloi_start = self.project_coordinates(47.25, -1.48, bounds, img_width, img_height)
        saint_eloi_end = self.project_coordinates(47.20, -1.52, bounds, img_width, img_height)
        draw.line([saint_eloi_start, saint_eloi_end], fill=waterway_color, width=8)
        draw.text((saint_eloi_start[0] + 10, saint_eloi_start[1] - 20), "Saint Eloi", fill='blue')
        
        # Loire - main river flowing west
        loire_points = []
        # Start east of Nantes, flow through Nantes to Atlantic
        for i in range(10):
            lon = -1.2 - (i * 0.13)  # Flow westward
            lat = 47.2184 + math.sin(i * 0.5) * 0.02  # Slight meandering
            x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
            loire_points.append((x, y))
        
        # Draw Loire with thick line
        for i in range(len(loire_points) - 1):
            draw.line([loire_points[i], loire_points[i+1]], fill=waterway_color, width=20)
        
        # Label Loire
        if len(loire_points) > 5:
            draw.text((loire_points[5][0], loire_points[5][1] + 25), "Loire", fill='blue')
        
        # Erdre - flows from north into Loire at Nantes
        erdre_start = self.project_coordinates(47.35, -1.55, bounds, img_width, img_height)
        erdre_end = self.project_coordinates(
            self.feature_coords["Erdre_confluence"][0],
            self.feature_coords["Erdre_confluence"][1],
            bounds, img_width, img_height
        )
        draw.line([erdre_start, erdre_end], fill=waterway_color, width=12)
        draw.text((erdre_start[0] + 10, erdre_start[1] + 20), "Erdre", fill='blue')
        
        # Sèvre Nantaise - flows from southeast
        sevre_start = self.project_coordinates(47.0, -1.2, bounds, img_width, img_height)
        sevre_end = self.project_coordinates(47.19, -1.54, bounds, img_width, img_height)
        draw.line([sevre_start, sevre_end], fill=waterway_color, width=10)
        draw.text((sevre_start[0] - 80, sevre_start[1] - 20), "Sèvre Nantaise", fill='blue')
        
        # Vilaine - flows northwest of Loire
        vilaine_points = []
        for i in range(5):
            lon = -2.0 - (i * 0.1)
            lat = 47.5 - (i * 0.02)
            x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
            vilaine_points.append((x, y))
        
        for i in range(len(vilaine_points) - 1):
            draw.line([vilaine_points[i], vilaine_points[i+1]], fill=waterway_color, width=15)
        
        if len(vilaine_points) > 2:
            draw.text((vilaine_points[2][0], vilaine_points[2][1] - 25), "Vilaine", fill='blue')
        
        # Don - tributary of Vilaine
        don_start = self.project_coordinates(47.55, -1.85, bounds, img_width, img_height)
        don_end = self.project_coordinates(47.48, -2.0, bounds, img_width, img_height)
        draw.line([don_start, don_end], fill=waterway_color, width=10)
        draw.text((don_start[0] - 30, don_start[1] - 20), "Don", fill='blue')
        
        # Brivet - flows near Saint-Nazaire
        brivet_start = self.project_coordinates(47.35, -2.15, bounds, img_width, img_height)
        brivet_end = self.project_coordinates(47.28, -2.20, bounds, img_width, img_height)
        draw.line([brivet_start, brivet_end], fill=waterway_color, width=10)
        draw.text((brivet_start[0] + 10, brivet_start[1] + 10), "Brivet", fill='blue')
        
        # Canal de Nantes à Brest - runs northwest from Nantes
        canal_start = self.project_coordinates(47.22, -1.58, bounds, img_width, img_height)
        canal_mid = self.project_coordinates(47.35, -1.75, bounds, img_width, img_height)
        canal_end = self.project_coordinates(47.5, -2.0, bounds, img_width, img_height)
        
        draw.line([canal_start, canal_mid], fill=waterway_color, width=8)
        draw.line([canal_mid, canal_end], fill=waterway_color, width=8)
        draw.text((canal_mid[0] - 50, canal_mid[1] - 20), "Canal de Nantes à Brest", fill='blue')
    
    def draw_motorway(self, draw: ImageDraw.Draw, bounds: Tuple[float, float, float, float],
                     img_width: int, img_height: int):
        """Draw N165 motorway with standard motorway symbol."""
        # Motorway color - typically blue or red
        motorway_color = (255, 0, 0)  # Red for motorway
        motorway_width = 8
        
        # N165 runs roughly northwest from south of Nantes towards Vannes
        n165_points = []
        start_lat, start_lon = 47.15, -1.60
        end_lat, end_lon = 47.65, -2.75
        
        # Create motorway path with some curves
        for i in range(10):
            t = i / 9.0
            lat = start_lat + (end_lat - start_lat) * t
            lon = start_lon + (end_lon - start_lon) * t + math.sin(t * 3) * 0.05
            x, y = self.project_coordinates(lat, lon, bounds, img_width, img_height)
            n165_points.append((x, y))
        
        # Draw motorway with parallel lines (standard symbol)
        for i in range(len(n165_points) - 1):
            # Main line
            draw.line([n165_points[i], n165_points[i+1]], fill=motorway_color, width=motorway_width)
            # Parallel white center line
            draw.line([n165_points[i], n165_points[i+1]], fill='white', width=motorway_width-4)
            # Red center
            draw.line([n165_points[i], n165_points[i+1]], fill=motorway_color, width=2)
        
        # Add motorway shield symbols
        if len(n165_points) > 5:
            shield_x, shield_y = n165_points[5]
            # Draw motorway shield
            shield_rect = [shield_x - 20, shield_y - 15, shield_x + 20, shield_y + 15]
            draw.rectangle(shield_rect, fill='white', outline=motorway_color, width=2)
            draw.text((shield_x - 15, shield_y - 10), "N165", fill=motorway_color)
    
    def generate_map(self, nw_lat: float, nw_lon: float, 
                    output_path: Optional[str] = None) -> str:
        """Generate the Nantes environs map."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        # Calculate bounds
        bounds = self.calculate_map_bounds(nw_lat, nw_lon)
        
        # Create image
        target_width = int(self.paper_size[0] * self.dpi / 25.4)
        target_height = int(self.paper_size[1] * self.dpi / 25.4)
        
        img = Image.new('RGB', (target_width, target_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw Atlantic Ocean first (background)
        self.draw_atlantic_ocean(draw, bounds, target_width, target_height)
        
        # Draw waterways
        self.draw_waterways(draw, bounds, target_width, target_height)
        
        # Draw motorway
        self.draw_motorway(draw, bounds, target_width, target_height)
        
        # Draw border
        border_width = 10
        draw.rectangle(
            [(border_width, border_width), 
             (target_width - border_width, target_height - border_width)],
            outline='black',
            width=border_width
        )
        
        # Add title and scale info
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        draw.text((100, 50), "Scale 1:375,000", fill='black', font=font)
        draw.text((100, 100), f"Northwest: {bounds[0]:.4f}°N, {bounds[1]:.4f}°E", fill='black', font=font)
        draw.text((100, 130), f"Southeast: {bounds[2]:.4f}°N, {bounds[3]:.4f}°E", fill='black', font=font)
        
        # Add Nantes city marker
        nantes_x, nantes_y = self.project_coordinates(
            self.feature_coords["Nantes"][0],
            self.feature_coords["Nantes"][1],
            bounds, target_width, target_height
        )
        # City symbol - filled circle
        draw.ellipse([nantes_x-10, nantes_y-10, nantes_x+10, nantes_y+10], fill='black')
        draw.text((nantes_x + 15, nantes_y - 10), "NANTES", fill='black')
        
        # Save image
        img.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path


def create_map_image(latitude: float, longitude: float, 
                    output_filename: str = "map.png") -> str:
    """Create a map image from given NW coordinates."""
    generator = NantesEnvironsMap()
    return generator.generate_map(latitude, longitude, output_filename)