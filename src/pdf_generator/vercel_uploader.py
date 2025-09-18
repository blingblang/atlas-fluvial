"""Vercel Blob Storage upload functionality."""

import os
import requests
from typing import Optional, Dict
from pathlib import Path
from datetime import datetime
import json


class VercelUploader:
    """Upload files to Vercel Blob Storage."""

    def __init__(self, token: Optional[str] = None):
        """Initialize Vercel uploader.

        Args:
            token: Vercel API token (can also be set via VERCEL_TOKEN or BLOB_READ_WRITE_TOKEN env var)
        """
        self.token = token or os.getenv('BLOB_READ_WRITE_TOKEN') or os.getenv('VERCEL_TOKEN')
        self.api_base = 'https://blob.vercel-storage.com'

        if not self.token:
            raise ValueError("Vercel token must be provided or set via BLOB_READ_WRITE_TOKEN or VERCEL_TOKEN environment variable")

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Vercel Blob API requests."""
        return {
            'Authorization': f'Bearer {self.token}',
        }

    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename with timestamp."""
        path = Path(original_filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_name = f"{path.stem}_{timestamp}{path.suffix}"
        return unique_name

    def upload_file(self, file_path: str, preserve_filename: bool = False, custom_filename: str = None) -> str:
        """Upload a file to Vercel Blob Storage.

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

        # Upload to Vercel Blob Storage
        upload_url = f"{self.api_base}/upload"

        headers = self._get_headers()
        headers['x-pathname'] = filename

        # Detect content type based on file extension
        ext = Path(file_path).suffix.lower()
        content_types = {
            '.pdf': 'application/pdf',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.html': 'text/html',
            '.json': 'application/json',
        }
        content_type = content_types.get(ext, 'application/octet-stream')
        headers['Content-Type'] = content_type

        response = requests.put(
            f"{upload_url}?filename={filename}",
            headers=headers,
            data=file_content
        )

        if response.status_code == 200:
            result = response.json()
            return result.get('url', f"{self.api_base}/{filename}")
        else:
            raise Exception(f"Upload failed: {response.status_code} - {response.text}")

    def upload_pdf(self, pdf_path: str, map_id: Optional[int] = None) -> str:
        """Upload a PDF file to Vercel Blob Storage.

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

    def list_files(self, prefix: Optional[str] = None) -> list:
        """List files in Vercel Blob Storage.

        Args:
            prefix: Optional prefix to filter files

        Returns:
            List of file metadata
        """
        list_url = f"{self.api_base}/list"
        headers = self._get_headers()

        params = {}
        if prefix:
            params['prefix'] = prefix

        response = requests.get(list_url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json().get('blobs', [])
        else:
            raise Exception(f"List failed: {response.status_code} - {response.text}")

    def delete_file(self, url: str) -> bool:
        """Delete a file from Vercel Blob Storage.

        Args:
            url: URL of the file to delete

        Returns:
            True if deletion was successful
        """
        delete_url = f"{self.api_base}/delete"
        headers = self._get_headers()
        headers['Content-Type'] = 'application/json'

        data = {"urls": [url]}

        response = requests.post(delete_url, headers=headers, json=data)

        return response.status_code == 200


def upload_to_vercel(file_path: str, token: Optional[str] = None, map_id: Optional[int] = None) -> str:
    """Upload a file to Vercel Blob Storage.

    Args:
        file_path: Path to the file to upload
        token: Vercel API token (optional if set in environment)
        map_id: Optional map ID for consistent naming

    Returns:
        Public URL of the uploaded file
    """
    uploader = VercelUploader(token)
    return uploader.upload_pdf(file_path, map_id=map_id)


# Compatibility alias for easy migration from Netlify
upload_to_storage = upload_to_vercel