"""Deploy Atlas Fluvial site to Vercel."""

import os
import sys
import subprocess
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

def check_vercel_cli():
    """Check if Vercel CLI is installed."""
    try:
        subprocess.run(["vercel", "--version"], check=True, capture_output=True, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Vercel CLI is not installed.")
        print("Please install it with: npm i -g vercel")
        return False

def build_site():
    """Build the Next.js site."""
    print("Building Atlas Fluvial site...")

    # Install dependencies
    print("Installing dependencies...")
    subprocess.run(["npm", "install"], check=True)

    # Build the site
    print("Building Next.js site...")
    subprocess.run(["npm", "run", "build"], check=True)

    print("Site built successfully!")
    return "out"  # Next.js export directory

def deploy_to_vercel(production=False):
    """Deploy the site to Vercel."""
    load_env()

    if not check_vercel_cli():
        return None

    print(f"Deploying to Vercel ({'production' if production else 'preview'})...")

    # Build the deployment command
    cmd = ["vercel", "--yes"]

    # Add production flag if needed
    if production:
        cmd.append("--prod")

    # Check if we have a token in environment
    vercel_token = os.getenv('VERCEL_TOKEN')
    if vercel_token:
        cmd.extend(["--token", vercel_token])

    try:
        # Run deployment
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Extract URL from output
        output_lines = result.stdout.strip().split('\n')
        for line in output_lines:
            if 'https://' in line:
                url = line.strip()
                if url.startswith('https://'):
                    return url

        # If we couldn't find a URL, return the last line (might be the URL)
        if output_lines:
            return output_lines[-1].strip()

        return "Deployment successful (URL not captured)"

    except subprocess.CalledProcessError as e:
        print(f"Deployment failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def setup_vercel_project():
    """Set up Vercel project configuration."""
    print("Setting up Vercel project...")

    # Check if vercel.json exists
    vercel_json_path = Path("vercel.json")
    if not vercel_json_path.exists():
        print("Creating vercel.json configuration...")
        config = {
            "buildCommand": "npm install && npm run build",
            "outputDirectory": "out",
            "framework": "nextjs",
            "installCommand": "npm install",
            "devCommand": "npm run dev"
        }
        with open(vercel_json_path, 'w') as f:
            json.dump(config, f, indent=2)
        print("Created vercel.json")

def main():
    """Main deployment function."""
    try:
        # Parse command line arguments
        production = "--prod" in sys.argv or "--production" in sys.argv

        # Change to site directory
        site_dir = Path(__file__).parent
        os.chdir(site_dir)

        # Setup Vercel project if needed
        setup_vercel_project()

        # Build the site
        build_dir = build_site()

        # Deploy to Vercel
        site_url = deploy_to_vercel(production=production)

        if site_url:
            print("\n✅ Deployment successful!")
            print(f"🌐 Site URL: {site_url}")
            if not production:
                print("\n💡 To deploy to production, run: python deploy_vercel.py --prod")
            print("\n⚠️  Note: The site may be gated with 'Coming Soon' popup.")
            print("To open the site, set NEXT_PUBLIC_GATE_OPEN=true in .env.local and redeploy.")
        else:
            print("\n❌ Deployment failed!")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()