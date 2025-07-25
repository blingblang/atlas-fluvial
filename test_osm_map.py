"""Test OSM-based map generation with accurate waterways."""

import os
from dotenv import load_dotenv
from src.pdf_generator.agent import PDFGeneratorAgent

# Load environment variables
load_dotenv()

def main():
    """Test the OSM-based map generator."""
    
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return
    
    if not os.getenv("NETLIFY_SITE_ID"):
        print("Error: NETLIFY_SITE_ID not set")
        return
    
    if not os.getenv("NETLIFY_ACCESS_TOKEN"):
        print("Error: NETLIFY_ACCESS_TOKEN not set")
        return
    
    # Create agent
    agent = PDFGeneratorAgent()
    
    # Generate Map 1 with accurate waterways
    map_id = 1
    print(f"Generating Map {map_id} with accurate waterway data from OpenStreetMap")
    print("Configuration:")
    print("- Center: 47.62685°N, -1.71915°W")
    print("- Scale: 1:375,000")
    print("- Features: Real river/canal geometries with curves and meanders")
    print("- Data source: OpenStreetMap Overpass API")
    print("\nThis may take a moment as we fetch real geographic data...")
    
    try:
        result = agent.generate_pdf(map_id)
        print(f"\nSuccess! PDF uploaded to Netlify")
        print(f"Public URL: {result['public_url']}")
        print(f"Generated at: {result['generated_at']}")
        print("\nThe waterways should now show accurate representations with:")
        print("- Natural curves and meanders for rivers")
        print("- Straight sections for canals")
        print("- Actual geographic paths from OSM data")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()