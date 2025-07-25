"""Generate maps with real waterway data from OpenStreetMap."""

import os
import math
import tempfile
import requests
from typing import Tuple, Optional, List, Dict
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json


class OSMWaterwayGenerator:
    """Generate maps with waterways from OpenStreetMap data."""
    
    def __init__(self):
        self.scale = 375000  # 1:375,000 scale
        self.paper_size = (210, 297)  # A4 in mm
        self.dpi = 300  # High quality for print
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        
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
    
    def fetch_waterways(self, bounds: Tuple[float, float, float, float]) -> List[Dict]:
        """Fetch waterway data from OpenStreetMap using Overpass API."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        
        # Overpass query for waterways
        query = f"""
        [out:json][timeout:25];
        (
          way["waterway"="river"]({se_lat},{nw_lon},{nw_lat},{se_lon});
          way["waterway"="stream"]({se_lat},{nw_lon},{nw_lat},{se_lon});
          way["waterway"="canal"]({se_lat},{nw_lon},{nw_lat},{se_lon});
          way["natural"="water"]({se_lat},{nw_lon},{nw_lat},{se_lon});
        );
        out geom;
        """
        
        try:
            response = requests.post(self.overpass_url, data=query)
            if response.status_code == 200:
                return response.json().get('elements', [])
        except Exception as e:
            print(f"Error fetching waterways: {e}")
        
        return []
    
    def project_coordinates(self, lat: float, lon: float, bounds: Tuple[float, float, float, float],
                          img_width: int, img_height: int) -> Tuple[int, int]:
        """Project lat/lon to pixel coordinates."""
        nw_lat, nw_lon, se_lat, se_lon = bounds
        
        # Simple linear projection
        x = int((lon - nw_lon) / (se_lon - nw_lon) * img_width)
        y = int((nw_lat - lat) / (nw_lat - se_lat) * img_height)
        
        return x, y
    
    def generate_map_with_waterways(self, nw_lat: float, nw_lon: float, 
                                   output_path: Optional[str] = None) -> str:
        """Generate a map with real waterway data."""
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
        
        # Fetch waterway data
        waterways = self.fetch_waterways(bounds)
        
        # Draw waterways
        waterway_color = (173, 216, 230)  # Light blue
        
        for waterway in waterways:
            if 'geometry' in waterway:
                coordinates = waterway['geometry']
                
                # Draw each waterway
                points = []
                for coord in coordinates:
                    x, y = self.project_coordinates(coord['lat'], coord['lon'], 
                                                  bounds, target_width, target_height)
                    points.append((x, y))
                
                # Determine width based on waterway type
                waterway_type = waterway.get('tags', {}).get('waterway', 'stream')
                width = {
                    'river': 15,
                    'canal': 12,
                    'stream': 8,
                }.get(waterway_type, 10)
                
                # Draw the waterway
                if len(points) > 1:
                    for i in range(len(points) - 1):
                        draw.line([points[i], points[i+1]], fill=waterway_color, width=width)
        
        # Add title and info
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        draw.text((100, 50), "OpenStreetMap - Waterways", fill='black', font=font)
        draw.text((100, 100), f"Northwest: {bounds[0]:.4f}°N, {bounds[1]:.4f}°E", fill='black', font=font)
        draw.text((100, 130), f"Southeast: {bounds[2]:.4f}°N, {bounds[3]:.4f}°E", fill='black', font=font)
        draw.text((100, 160), f"Scale: 1:{self.scale:,}", fill='black', font=font)
        draw.text((100, target_height - 50), f"Waterways: {len(waterways)} features", fill='blue', font=font)
        
        # Save image
        img.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path
    
    def generate_map(self, nw_lat: float, nw_lon: float, 
                    output_path: Optional[str] = None) -> str:
        """Generate a map image from coordinates."""
        try:
            # Try to fetch real data
            return self.generate_map_with_waterways(nw_lat, nw_lon, output_path)
        except Exception as e:
            print(f"Error generating map with OSM data: {e}")
            # Fall back to simple generator
            from .simple_map_generator import SimpleMapGenerator
            generator = SimpleMapGenerator()
            return generator.generate_map(nw_lat, nw_lon, output_path)


def create_map_image(latitude: float, longitude: float, 
                    output_filename: str = "map.png") -> str:
    """Create a map image from given NW coordinates."""
    generator = OSMWaterwayGenerator()
    return generator.generate_map(latitude, longitude, output_filename)