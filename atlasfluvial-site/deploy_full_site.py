"""Deploy the full Atlas Fluvial site to Netlify."""

import os
import requests
import zipfile
from pathlib import Path

def load_env():
    """Load environment variables."""
    parent_env = Path(__file__).parent.parent / '.env'
    if parent_env.exists():
        with open(parent_env, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")

def create_zip(directory):
    """Create a zip file of the directory."""
    print(f"Creating zip file from {directory}...")
    zip_path = "deploy.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, directory)
                zipf.write(file_path, arc_path)
    
    return zip_path

def deploy_to_netlify(zip_path):
    """Deploy to Netlify."""
    load_env()
    
    site_id = os.getenv('NETLIFY_SITE_ID')
    access_token = os.getenv('NETLIFY_ACCESS_TOKEN')
    
    if not site_id or not access_token:
        print("Error: Missing Netlify credentials")
        return None
    
    print("Deploying to Netlify...")
    
    url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/zip'
    }
    
    with open(zip_path, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
    
    if response.status_code in [200, 201]:
        deploy_data = response.json()
        site_url = deploy_data.get('ssl_url') or deploy_data.get('url')
        print(f"Successfully deployed!")
        print(f"Site URL: {site_url}")
        return site_url
    else:
        print(f"Deployment failed: {response.status_code}")
        print(response.text)
        return None

def main():
    """Main deployment."""
    try:
        # Check if out directory exists
        out_dir = Path("out")
        if not out_dir.exists():
            print("Error: 'out' directory not found. Run create_static_site.py first.")
            return
        
        # Create zip
        zip_path = create_zip(str(out_dir))
        
        # Deploy
        site_url = deploy_to_netlify(zip_path)
        
        # Cleanup
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        if site_url:
            print("\nDeployment successful!")
            print(f"Atlas Fluvial is live at: {site_url}")
            print("\nThe coming soon gate is now OPEN - you can browse the full site!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()