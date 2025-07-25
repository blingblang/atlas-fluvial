"""Generate maps showing only specific navigable waterways."""

import os
import math
import tempfile
import requests
from typing import Tuple, Optional, List, Dict, Set
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json


class NavigableWaterwaysGenerator:
    """Generate maps with specific navigable waterways from OpenStreetMap data."""
    
    def __init__(self):
        self.scale = 375000  # 1:375,000 scale
        self.paper_size = (210, 297)  # A4 in mm
        self.dpi = 300  # High quality for print
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Specific navigable waterways to show
        self.navigable_waterways = {
            "Vilaine", "Brivet", "Canal de Nantes à Brest", "Canal de Nantes a Brest",
            "Erdre", "Loire", "Sèvre Nantaise", "Sevre Nantaise", "Don"
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
    
    def fetch_navigable_waterways(self, bounds: Tuple[float, float, float, float]) -> List[Dict]:
        """Fetch specific navigable waterway data from OpenStreetMap."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        
        # Build name filter for Overpass query
        name_filters = '|'.join(self.navigable_waterways)
        
        # Overpass query for specific waterways
        query = f"""
        [out:json][timeout:30];
        (
          way["waterway"]["name"~"^({name_filters})$"]({se_lat},{nw_lon},{nw_lat},{se_lon});
          way["waterway"]["name:en"~"^({name_filters})$"]({se_lat},{nw_lon},{nw_lat},{se_lon});
          way["waterway"]["name:fr"~"^({name_filters})$"]({se_lat},{nw_lon},{nw_lat},{se_lon});
          relation["waterway"]["name"~"^({name_filters})$"]({se_lat},{nw_lon},{nw_lat},{se_lon});
        );
        out geom;
        """
        
        try:
            response = requests.post(self.overpass_url, data=query, timeout=30)
            if response.status_code == 200:
                return response.json().get('elements', [])
            else:
                print(f"Overpass API error: {response.status_code}")
        except Exception as e:
            print(f"Error fetching waterways: {e}")
        
        return []
    
    def is_navigable_waterway(self, tags: Dict) -> bool:
        """Check if waterway name matches our navigable list."""
        name = tags.get('name', '')
        name_en = tags.get('name:en', '')
        name_fr = tags.get('name:fr', '')
        
        for waterway_name in [name, name_en, name_fr]:
            if waterway_name in self.navigable_waterways:
                return True
        
        return False
    
    def project_coordinates(self, lat: float, lon: float, bounds: Tuple[float, float, float, float],
                          img_width: int, img_height: int) -> Tuple[int, int]:
        """Project lat/lon to pixel coordinates."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        
        # Simple linear projection
        x = int((lon - nw_lon) / (se_lon - nw_lon) * img_width)
        y = int((nw_lat - lat) / (nw_lat - se_lat) * img_height)
        
        return x, y
    
    def generate_placeholder_waterways(self, bounds: Tuple[float, float, float, float],
                                     img_width: int, img_height: int, draw: ImageDraw.Draw):
        """Generate placeholder waterways based on the region."""
        waterway_color = (173, 216, 230)  # Light blue
        
        # This is a simplified representation - actual waterways would come from OSM
        # Loire (main river)
        loire_points = []
        for i in range(0, img_width, 30):
            y = int(img_height * 0.4 + math.sin(i * 0.01) * 50)
            loire_points.append((i, y))
        
        for i in range(len(loire_points) - 1):
            draw.line([loire_points[i], loire_points[i+1]], fill=waterway_color, width=20)
        
        # Vilaine
        vilaine_start = (int(img_width * 0.1), int(img_height * 0.2))
        vilaine_end = (int(img_width * 0.5), int(img_height * 0.35))
        draw.line([vilaine_start, vilaine_end], fill=waterway_color, width=15)
        
        # Erdre
        erdre_start = (int(img_width * 0.6), int(img_height * 0.1))
        erdre_end = (int(img_width * 0.55), int(img_height * 0.4))
        draw.line([erdre_start, erdre_end], fill=waterway_color, width=12)
        
        # Canal de Nantes à Brest
        canal_points = [
            (int(img_width * 0.2), int(img_height * 0.6)),
            (int(img_width * 0.4), int(img_height * 0.55)),
            (int(img_width * 0.6), int(img_height * 0.5))
        ]
        for i in range(len(canal_points) - 1):
            draw.line([canal_points[i], canal_points[i+1]], fill=waterway_color, width=10)
        
        # Add labels
        font = None
        try:
            font = ImageFont.load_default()
        except:
            pass
        
        draw.text((loire_points[len(loire_points)//2][0], loire_points[len(loire_points)//2][1] + 25), 
                 "Loire", fill='blue', font=font)
        draw.text((vilaine_start[0] + 20, vilaine_start[1] + 20), "Vilaine", fill='blue', font=font)
        draw.text((erdre_start[0] - 50, erdre_start[1] + 20), "Erdre", fill='blue', font=font)
        draw.text((canal_points[1][0], canal_points[1][1] + 15), "Canal de Nantes à Brest", fill='blue', font=font)
    
    def generate_map_with_navigable_waterways(self, nw_lat: float, nw_lon: float, 
                                            output_path: Optional[str] = None) -> str:
        """Generate a map with only navigable waterways."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        # Calculate bounds
        bounds = self.calculate_map_bounds(nw_lat, nw_lon)
        
        # Create image
        target_width = int(self.paper_size[0] * self.dpi / 25.4)
        target_height = int(self.paper_size[1] * self.dpi / 25.4)
        
        img = Image.new('RGB', (target_width, target_height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw border
        border_width = 10
        draw.rectangle(
            [(border_width, border_width), 
             (target_width - border_width, target_height - border_width)],
            outline='black',
            width=border_width
        )
        
        # Try to fetch real waterway data
        waterways = self.fetch_navigable_waterways(bounds)
        
        if waterways:
            # Draw real waterways from OSM
            waterway_color = (173, 216, 230)  # Light blue
            drawn_waterways = set()
            
            for waterway in waterways:
                tags = waterway.get('tags', {})
                waterway_name = tags.get('name', tags.get('name:fr', ''))
                
                if self.is_navigable_waterway(tags) and 'geometry' in waterway:
                    coordinates = waterway['geometry']
                    
                    # Draw waterway
                    points = []
                    for coord in coordinates:
                        x, y = self.project_coordinates(coord['lat'], coord['lon'], 
                                                      bounds, target_width, target_height)
                        points.append((x, y))
                    
                    # Determine width based on waterway
                    width = 15 if waterway_name == 'Loire' else 12
                    
                    # Draw the waterway
                    if len(points) > 1:
                        for i in range(len(points) - 1):
                            draw.line([points[i], points[i+1]], fill=waterway_color, width=width)
                        
                        # Add label
                        if waterway_name and waterway_name not in drawn_waterways:
                            mid_point = points[len(points)//2]
                            draw.text((mid_point[0], mid_point[1] + 20), 
                                    waterway_name, fill='blue')
                            drawn_waterways.add(waterway_name)
        else:
            # Use placeholder waterways
            self.generate_placeholder_waterways(bounds, target_width, target_height, draw)
        
        # Add title and info
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        draw.text((100, 50), "Navigable Waterways", fill='black', font=font)
        draw.text((100, 100), f"Northwest: {bounds[0]:.4f}°N, {bounds[1]:.4f}°E", fill='black', font=font)
        draw.text((100, 130), f"Southeast: {bounds[2]:.4f}°N, {bounds[3]:.4f}°E", fill='black', font=font)
        draw.text((100, 160), f"Scale: 1:{self.scale:,}", fill='black', font=font)
        
        # List navigable waterways
        waterway_list = "Showing: " + ", ".join(sorted(self.navigable_waterways))
        draw.text((100, target_height - 80), waterway_list[:60] + "...", fill='blue', font=font)
        if len(waterway_list) > 60:
            draw.text((100, target_height - 50), waterway_list[60:], fill='blue', font=font)
        
        # Save image
        img.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path
    
    def generate_map(self, nw_lat: float, nw_lon: float, 
                    output_path: Optional[str] = None) -> str:
        """Generate a map image from coordinates."""
        return self.generate_map_with_navigable_waterways(nw_lat, nw_lon, output_path)


def create_map_image(latitude: float, longitude: float, 
                    output_filename: str = "map.png") -> str:
    """Create a map image from given NW coordinates."""
    generator = NavigableWaterwaysGenerator()
    return generator.generate_map(latitude, longitude, output_filename)