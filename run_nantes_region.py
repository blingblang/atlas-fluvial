"""Run the PDF generator with correct coordinates for Nantes region."""

import os
from dotenv import load_dotenv
from src.pdf_generator.agent import PDFGeneratorAgent

# Load environment variables
load_dotenv()

# Coordinates for Nantes region (negative longitude for west)
LATITUDE = 47.9797
LONGITUDE = -2.0836  # Changed to negative for west of Greenwich

def main():
    """Run the PDF generator agent with Nantes region coordinates."""
    
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
    
    print(f"Generating PDF with map from coordinates:")
    print(f"  Northwest corner: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"  Scale: 1:375,000")
    print(f"  Paper size: A4 (landscape)")
    print(f"  This should properly show Nantes and surrounding waterways")
    
    # Create agent
    agent = PDFGeneratorAgent()
    
    # Generate PDF
    print("\nRunning agent to generate PDF...")
    try:
        result = agent.generate_pdf(LATITUDE, LONGITUDE)
        print(f"\nSuccess! PDF uploaded to Netlify")
        print(f"Public URL: {result['public_url']}")
        print(f"Generated at: {result['generated_at']}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()