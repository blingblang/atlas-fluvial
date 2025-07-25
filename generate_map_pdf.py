"""Generate a Map PDF and upload to Netlify."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from src.pdf_generator.agent import PDFGeneratorAgent

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

def main():
    """Generate PDF for specified map ID."""
    map_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print(f"Generating PDF for Map {map_id}...")
    
    # Initialize agent
    agent = PDFGeneratorAgent()
    
    # Generate PDF
    result = agent.generate_pdf(map_id)
    
    print(f"PDF generated and uploaded successfully!")
    print(f"Result: {result}")
    
    # Extract URL from result
    if 'output' in result:
        print(f"\nPDF URL: {result['output']}")

if __name__ == "__main__":
    main()