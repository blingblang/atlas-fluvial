"""Simple map generator using static map services (no Selenium required)."""

import os
import math
import tempfile
import requests
from typing import Tuple, Optional
from PIL import Image
from io import BytesIO


class SimpleMapGenerator:
    """Generate maps using static map APIs."""
    
    def __init__(self):
        self.scale = 375000  # 1:375,000 scale
        self.paper_size = (297, 210)  # A4 landscape in mm
        self.dpi = 300  # High quality for print
        
    def calculate_map_bounds(self, nw_lat: float, nw_lon: float) -> Tuple[float, float, float, float]:
        """Calculate SE corner based on NW corner and A4 paper size at given scale."""
        # Convert paper dimensions to meters
        paper_width_m = (self.paper_size[0] / 1000) * self.scale  # mm to m, then scale
        paper_height_m = (self.paper_size[1] / 1000) * self.scale
        
        # Earth's radius in meters
        earth_radius = 6371000
        
        # Calculate latitude change (simple since we're moving south)
        lat_change = (paper_height_m / earth_radius) * (180 / math.pi)
        se_lat = nw_lat - lat_change
        
        # Calculate longitude change (accounting for latitude)
        avg_lat = (nw_lat + se_lat) / 2
        lon_change = (paper_width_m / (earth_radius * math.cos(math.radians(avg_lat)))) * (180 / math.pi)
        se_lon = nw_lon + lon_change
        
        return nw_lat, nw_lon, se_lat, se_lon
    
    def generate_placeholder_map(self, nw_lat: float, nw_lon: float, 
                                output_path: Optional[str] = None) -> str:
        """Generate a placeholder map image with coordinate information."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        # Calculate bounds
        bounds = self.calculate_map_bounds(nw_lat, nw_lon)
        
        # Create a placeholder image
        target_width = int(self.paper_size[0] * self.dpi / 25.4)  # mm to inches to pixels
        target_height = int(self.paper_size[1] * self.dpi / 25.4)
        
        # Create white background
        img = Image.new('RGB', (target_width, target_height), 'white')
        
        # Add text overlay using PIL
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        
        # Try to use a basic font
        try:
            # Use default font
            font_size = 48
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw border
        border_width = 10
        draw.rectangle(
            [(border_width, border_width), 
             (target_width - border_width, target_height - border_width)],
            outline='black',
            width=border_width
        )
        
        # Add text information
        text_lines = [
            "OpenStreetMap Placeholder",
            f"Northwest: {bounds[0]:.4f}°N, {bounds[1]:.4f}°E",
            f"Southeast: {bounds[2]:.4f}°N, {bounds[3]:.4f}°E",
            f"Scale: 1:{self.scale:,}",
            "Map data would show waterways and locks"
        ]
        
        y_position = 100
        for line in text_lines:
            draw.text((100, y_position), line, fill='black', font=font)
            y_position += 60
        
        # Draw a simple grid to represent map features
        grid_size = 100
        for x in range(0, target_width, grid_size):
            draw.line([(x, 0), (x, target_height)], fill='lightgray', width=1)
        for y in range(0, target_height, grid_size):
            draw.line([(0, y), (target_width, y)], fill='lightgray', width=1)
        
        # Draw simulated waterways in light blue
        # These are placeholder waterways - in production, you'd fetch real data
        waterway_color = (173, 216, 230)  # Light blue RGB
        
        # Draw main river (diagonal across map)
        river_points = []
        for i in range(0, target_width, 50):
            y = int(target_height * 0.3 + (i / target_width) * target_height * 0.4)
            river_points.append((i, y))
        
        # Draw river with varying width
        for i in range(len(river_points) - 1):
            width = 15 + int(10 * math.sin(i * 0.1))  # Varying width
            draw.line([river_points[i], river_points[i+1]], fill=waterway_color, width=width)
        
        # Draw tributary
        tributary_start = (int(target_width * 0.7), 0)
        tributary_end = (int(target_width * 0.5), int(target_height * 0.5))
        draw.line([tributary_start, tributary_end], fill=waterway_color, width=12)
        
        # Draw another waterway
        waterway2_points = [
            (int(target_width * 0.2), int(target_height * 0.8)),
            (int(target_width * 0.3), int(target_height * 0.7)),
            (int(target_width * 0.4), int(target_height * 0.75)),
            (int(target_width * 0.6), int(target_height * 0.6))
        ]
        for i in range(len(waterway2_points) - 1):
            draw.line([waterway2_points[i], waterway2_points[i+1]], fill=waterway_color, width=10)
        
        # Add label for waterways
        draw.text((100, target_height - 100), "Waterways shown in light blue", fill='blue', font=font)
        
        # Save image
        img.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path
    
    def generate_map(self, nw_lat: float, nw_lon: float, 
                    output_path: Optional[str] = None) -> str:
        """Generate a map image from coordinates."""
        # For now, use placeholder. In production, you could use:
        # - OpenStreetMap Static API
        # - Mapbox Static API
        # - Google Maps Static API
        return self.generate_placeholder_map(nw_lat, nw_lon, output_path)


def create_map_image(latitude: float, longitude: float, 
                    output_filename: str = "map.png") -> str:
    """Create a map image from given NW coordinates."""
    generator = SimpleMapGenerator()
    return generator.generate_map(latitude, longitude, output_filename)