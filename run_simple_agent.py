"""Simple script to run the PDF generation with Netlify upload."""

import os
from dotenv import load_dotenv
from src.pdf_generator.agent import PDFGeneratorAgent

# Load environment variables
load_dotenv()

# Coordinates
LATITUDE = 47.9797
LONGITUDE = 2.0836

def main():
    """Run the PDF generator agent."""
    
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
    print(f"  Paper size: A4")
    
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