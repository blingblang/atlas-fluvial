"""Run the PDF generation agent with map configuration."""

import os
from dotenv import load_dotenv
from src.pdf_generator.agent import PDFGeneratorAgent

# Load environment variables
load_dotenv()

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
    
    print("Generating PDF for Map 1: Nantes and environs")
    print("  Scale: 1:375,000")
    print("  Paper size: A4 landscape")
    
    # Create agent
    agent = PDFGeneratorAgent()
    
    # Generate PDF for map ID 1
    print("\nRunning agent to generate PDF...")
    try:
        result = agent.generate_pdf(map_id=1)
        print(f"\nSuccess! PDF uploaded to Netlify")
        print(f"Public URL: {result['public_url']}")
        print(f"Generated at: {result['generated_at']}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()