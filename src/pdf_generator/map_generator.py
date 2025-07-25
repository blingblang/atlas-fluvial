"""OpenStreetMap integration for generating map images."""

import os
from typing import Tuple, Optional
from pathlib import Path
import tempfile
import math

import folium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image
import time


class MapGenerator:
    """Generate maps using OpenStreetMap data."""
    
    def __init__(self):
        self.scale = 375000  # 1:375,000 scale
        self.paper_size = (210, 297)  # A4 in mm
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
    
    def generate_map_html(self, nw_lat: float, nw_lon: float, 
                         output_path: Optional[str] = None) -> str:
        """Generate an HTML map using Folium."""
        # Calculate bounds
        bounds = self.calculate_map_bounds(nw_lat, nw_lon)
        nw_corner = [bounds[0], bounds[1]]
        se_corner = [bounds[2], bounds[3]]
        
        # Calculate center
        center_lat = (bounds[0] + bounds[2]) / 2
        center_lon = (bounds[1] + bounds[3]) / 2
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=10,
            tiles='OpenStreetMap',
            prefer_canvas=True
        )
        
        # Fit to bounds
        m.fit_bounds([nw_corner, se_corner])
        
        # Add scale control
        folium.plugins.MeasureControl(position='bottomleft').add_to(m)
        
        # Add markers for corners (optional, for debugging)
        folium.Marker(
            nw_corner,
            popup="NW Corner",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
        
        folium.Marker(
            se_corner,
            popup="SE Corner",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
        
        # Save HTML
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.html')
        
        m.save(output_path)
        return output_path
    
    def html_to_image(self, html_path: str, output_path: Optional[str] = None) -> str:
        """Convert HTML map to image using Selenium."""
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.png')
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--window-size={self.paper_size[0]*4},{self.paper_size[1]*4}')
        
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # Load the HTML file
            driver.get(f'file:///{os.path.abspath(html_path)}')
            
            # Wait for map to load
            time.sleep(3)
            
            # Take screenshot
            driver.save_screenshot(output_path)
            
        finally:
            driver.quit()
        
        # Resize to exact A4 dimensions at high DPI
        img = Image.open(output_path)
        target_width = int(self.paper_size[0] * self.dpi / 25.4)  # mm to inches to pixels
        target_height = int(self.paper_size[1] * self.dpi / 25.4)
        
        img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        img_resized.save(output_path, dpi=(self.dpi, self.dpi))
        
        return output_path
    
    def generate_map(self, nw_lat: float, nw_lon: float, 
                    output_path: Optional[str] = None) -> str:
        """Generate a map image from coordinates."""
        # Generate HTML map
        html_path = self.generate_map_html(nw_lat, nw_lon)
        
        # Convert to image
        image_path = self.html_to_image(html_path, output_path)
        
        # Clean up temporary HTML
        if os.path.exists(html_path):
            os.remove(html_path)
        
        return image_path


def create_map_image(latitude: float, longitude: float, 
                    output_filename: str = "map.png") -> str:
    """Create a map image from given NW coordinates."""
    generator = MapGenerator()
    return generator.generate_map(latitude, longitude, output_filename)