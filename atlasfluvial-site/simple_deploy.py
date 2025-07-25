"""Simple deployment to Netlify without npm build."""

import os
import requests
import zipfile
import json
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

def create_deployment_files():
    """Create a simple index.html for initial deployment."""
    print("Creating deployment files...")
    
    # Create public directory
    public_dir = Path("public")
    public_dir.mkdir(exist_ok=True)
    
    # Create a simple holding page
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atlas Fluvial - Coming Soon</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0064C8 0%, #0078DC 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            padding: 2rem;
            max-width: 600px;
        }
        h1 { font-size: 3rem; margin-bottom: 1rem; }
        p { font-size: 1.25rem; margin-bottom: 2rem; opacity: 0.9; }
        .coming-soon {
            display: inline-block;
            padding: 1rem 2rem;
            background: white;
            color: #0064C8;
            border-radius: 8px;
            font-weight: bold;
            text-decoration: none;
            transition: transform 0.2s;
        }
        .coming-soon:hover { transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <h1>Atlas Fluvial</h1>
        <p>Your comprehensive guide to European waterways</p>
        <div class="coming-soon">Coming Soon</div>
    </div>
</body>
</html>"""
    
    with open(public_dir / "index.html", "w") as f:
        f.write(index_html)
    
    # Create _redirects file for SPA routing
    redirects = """/*    /index.html    200"""
    with open(public_dir / "_redirects", "w") as f:
        f.write(redirects)
    
    return str(public_dir)

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
        # Create deployment files
        deploy_dir = create_deployment_files()
        
        # Create zip
        zip_path = create_zip(deploy_dir)
        
        # Deploy
        site_url = deploy_to_netlify(zip_path)
        
        # Cleanup
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        if site_url:
            print("\nDeployment successful!")
            print(f"Atlas Fluvial is live at: {site_url}")
            print("\nNote: This is a placeholder page. The full Next.js site requires npm to build.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()