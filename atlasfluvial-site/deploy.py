"""Deploy Atlas Fluvial site to Netlify."""

import os
import sys
import subprocess
import requests
import zipfile
import json
from pathlib import Path

def load_env():
    """Load environment variables from parent .env file."""
    parent_env = Path(__file__).parent.parent / '.env'
    if parent_env.exists():
        with open(parent_env, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")

def build_site():
    """Build the Next.js site."""
    print("Building Atlas Fluvial site...")
    
    # Install dependencies
    print("Installing dependencies...")
    subprocess.run(["npm", "install"], check=True)
    
    # Build the site
    print("Building Next.js site...")
    subprocess.run(["npm", "run", "build"], check=True)
    subprocess.run(["npm", "run", "export"], check=True)
    
    print("Site built successfully!")
    return "out"  # Next.js export directory

def create_zip(directory):
    """Create a zip file of the build directory."""
    print(f"Creating zip file from {directory}...")
    zip_path = "atlasfluvial-site.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, directory)
                zipf.write(file_path, arc_path)
    
    print(f"Created {zip_path}")
    return zip_path

def deploy_to_netlify(zip_path):
    """Deploy the site to Netlify."""
    load_env()
    
    site_id = os.getenv('NETLIFY_SITE_ID')
    access_token = os.getenv('NETLIFY_ACCESS_TOKEN')
    
    if not site_id or not access_token:
        print("Error: NETLIFY_SITE_ID and NETLIFY_ACCESS_TOKEN must be set")
        return None
    
    print("Deploying to Netlify...")
    
    # Create a new site deployment
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
        print(f"Successfully deployed to: {site_url}")
        print(f"Deploy ID: {deploy_data.get('id')}")
        return site_url
    else:
        print(f"Deployment failed: {response.status_code}")
        print(response.text)
        return None

def main():
    """Main deployment function."""
    try:
        # Change to site directory
        site_dir = Path(__file__).parent
        os.chdir(site_dir)
        
        # Build the site
        build_dir = build_site()
        
        # Create zip file
        zip_path = create_zip(build_dir)
        
        # Deploy to Netlify
        site_url = deploy_to_netlify(zip_path)
        
        # Clean up
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        if site_url:
            print("\n✅ Deployment successful!")
            print(f"🌐 Site URL: {site_url}")
            print("\n⚠️  Note: The site is currently gated with 'Coming Soon' popup.")
            print("To open the site, set NEXT_PUBLIC_GATE_OPEN=true in .env.local and redeploy.")
        else:
            print("\n❌ Deployment failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()