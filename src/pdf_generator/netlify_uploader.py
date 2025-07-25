"""Netlify CDN upload functionality."""

import os
import requests
from typing import Optional, Dict
from pathlib import Path
import hashlib
from datetime import datetime


class NetlifyUploader:
    """Upload files to Netlify CDN."""
    
    def __init__(self, site_id: Optional[str] = None, access_token: Optional[str] = None):
        """Initialize Netlify uploader.
        
        Args:
            site_id: Netlify site ID (can also be set via NETLIFY_SITE_ID env var)
            access_token: Netlify access token (can also be set via NETLIFY_ACCESS_TOKEN env var)
        """
        self.site_id = site_id or os.getenv('NETLIFY_SITE_ID')
        self.access_token = access_token or os.getenv('NETLIFY_ACCESS_TOKEN')
        self.api_base = 'https://api.netlify.com/api/v1'
        
        if not self.site_id:
            raise ValueError("Netlify site ID must be provided or set via NETLIFY_SITE_ID environment variable")
        if not self.access_token:
            raise ValueError("Netlify access token must be provided or set via NETLIFY_ACCESS_TOKEN environment variable")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Netlify API requests."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/octet-stream'
        }
    
    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename with timestamp."""
        path = Path(original_filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_name = f"{path.stem}_{timestamp}{path.suffix}"
        return unique_name
    
    def upload_file(self, file_path: str, preserve_filename: bool = False, custom_filename: str = None) -> str:
        """Upload a file to Netlify CDN.
        
        Args:
            file_path: Path to the file to upload
            preserve_filename: If True, keeps original filename; if False, adds timestamp
            custom_filename: Optional custom filename to use
            
        Returns:
            Public URL of the uploaded file
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine filename
        if custom_filename:
            filename = custom_filename
        else:
            filename = os.path.basename(file_path)
            if not preserve_filename:
                filename = self._generate_unique_filename(filename)
        
        # Read file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Calculate file hash
        file_hash = hashlib.sha1(file_content).hexdigest()
        
        # Create deploy
        deploy_url = f"{self.api_base}/sites/{self.site_id}/deploys"
        deploy_data = {
            "files": {
                f"/{filename}": file_hash
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(deploy_url, json=deploy_data, headers=headers)
        response.raise_for_status()
        deploy_id = response.json()['id']
        
        # Upload the file
        upload_url = f"{self.api_base}/deploys/{deploy_id}/files/{filename}"
        
        headers = self._get_headers()
        response = requests.put(upload_url, data=file_content, headers=headers)
        response.raise_for_status()
        
        # Get the site info to construct the public URL
        site_url = f"{self.api_base}/sites/{self.site_id}"
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.get(site_url, headers=headers)
        response.raise_for_status()
        site_info = response.json()
        
        # Construct public URL
        site_name = site_info.get('name') or site_info.get('subdomain')
        public_url = f"https://{site_name}.netlify.app/{filename}"
        
        return public_url
    
    def upload_pdf(self, pdf_path: str, map_id: Optional[int] = None) -> str:
        """Upload a PDF file to Netlify CDN.
        
        Args:
            pdf_path: Path to the PDF file
            map_id: Optional map ID for consistent naming
            
        Returns:
            Public URL of the uploaded PDF
        """
        if map_id == 1:
            # Use consistent naming for Map 1
            return self.upload_file(pdf_path, custom_filename="map_1_latest.pdf")
        else:
            return self.upload_file(pdf_path, preserve_filename=False)


def upload_to_netlify(file_path: str, site_id: Optional[str] = None, 
                     access_token: Optional[str] = None, map_id: Optional[int] = None) -> str:
    """Upload a file to Netlify CDN.
    
    Args:
        file_path: Path to the file to upload
        site_id: Netlify site ID (optional if set in environment)
        access_token: Netlify access token (optional if set in environment)
        map_id: Optional map ID for consistent naming
        
    Returns:
        Public URL of the uploaded file
    """
    uploader = NetlifyUploader(site_id, access_token)
    return uploader.upload_pdf(file_path, map_id=map_id)