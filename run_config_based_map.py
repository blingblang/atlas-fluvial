"""Run the configuration-based PDF generator."""

import os
from dotenv import load_dotenv
from src.pdf_generator.agent import PDFGeneratorAgent

# Load environment variables
load_dotenv()

def main():
    """Run the PDF generator agent with configuration-based maps."""
    
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
    
    # Generate Map 1: Nantes and environs
    map_id = 1
    print(f"Generating PDF for Map {map_id}")
    print("This map will be centered on Nantes with configuration from JSON file")
    print("- Center: 47.2184°N, -1.5536°E")
    print("- Scale: 1:375,000")
    print("- Slope: 0° (parallel of latitude)")
    print("- Paper: A4 landscape")
    
    try:
        result = agent.generate_pdf(map_id)
        print(f"\nSuccess! PDF uploaded to Netlify")
        print(f"Public URL: {result['public_url']}")
        print(f"Generated at: {result['generated_at']}")
        print(f"Map ID: {result['map_id']}")
    except Exception as e:
        print(f"\nError: {e}")
    
    # Test Map 21 with 45° rotation
    print("\n" + "="*60 + "\n")
    map_id = 21
    print(f"Generating PDF for Map {map_id} (with 45° rotation)")
    print("This map will demonstrate the slope/rotation feature")
    print("- Center: 47.1650°N, -1.3700°E")
    print("- Scale: 1:150,000")
    print("- Slope: 45° (diagonal orientation)")
    
    try:
        result = agent.generate_pdf(map_id)
        print(f"\nSuccess! PDF uploaded to Netlify")
        print(f"Public URL: {result['public_url']}")
        print(f"Generated at: {result['generated_at']}")
        print(f"Map ID: {result['map_id']}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()