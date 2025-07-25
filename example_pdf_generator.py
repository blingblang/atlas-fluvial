"""Example script demonstrating PDF generation with map."""

import os
from dotenv import load_dotenv
from src.pdf_generator.langgraph_agent import create_ambient_pdf_generator

# Load environment variables from .env file
load_dotenv()

# Coordinates for map generation
LATITUDE = 47.9797  # Northwest corner latitude
LONGITUDE = 2.0836  # Northwest corner longitude

def run_example():
    """Run a single PDF generation example."""
    
    # Ensure environment variables are set
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    if not os.getenv("NETLIFY_SITE_ID"):
        print("Please set NETLIFY_SITE_ID environment variable")
        return
    
    if not os.getenv("NETLIFY_ACCESS_TOKEN"):
        print("Please set NETLIFY_ACCESS_TOKEN environment variable")
        return
    
    print(f"Generating PDF with map from coordinates:")
    print(f"  Northwest corner: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"  Scale: 1:375,000")
    print(f"  Paper size: A4")
    
    # Create the generator
    generator = create_ambient_pdf_generator(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        regeneration_hours=24
    )
    
    # Run once
    print("\nGenerating PDF...")
    result = generator.run_once()
    
    if result.get("public_url"):
        print(f"\nPDF generated successfully!")
        print(f"Public URL: {result['public_url']}")
        print(f"Generated at: {result['generated_at']}")
    else:
        print("\nFailed to generate PDF")


if __name__ == "__main__":
    run_example()