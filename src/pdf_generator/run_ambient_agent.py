"""Main script to run the ambient PDF generator."""

import os
import asyncio
import argparse
import logging
from typing import Optional
from dotenv import load_dotenv

from .langgraph_agent import create_ambient_pdf_generator

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run the ambient PDF generator."""
    parser = argparse.ArgumentParser(description="Run ambient PDF generator")
    parser.add_argument("--latitude", type=float, required=True,
                       help="Northwest corner latitude")
    parser.add_argument("--longitude", type=float, required=True,
                       help="Northwest corner longitude")
    parser.add_argument("--interval", type=int, default=24,
                       help="Regeneration interval in hours (default: 24)")
    parser.add_argument("--once", action="store_true",
                       help="Run once instead of continuously")
    parser.add_argument("--openai-key", type=str, default=None,
                       help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--netlify-site", type=str, default=None,
                       help="Netlify site ID (or set NETLIFY_SITE_ID env var)")
    parser.add_argument("--netlify-token", type=str, default=None,
                       help="Netlify access token (or set NETLIFY_ACCESS_TOKEN env var)")
    
    args = parser.parse_args()
    
    # Set environment variables if provided
    if args.openai_key:
        os.environ["OPENAI_API_KEY"] = args.openai_key
    if args.netlify_site:
        os.environ["NETLIFY_SITE_ID"] = args.netlify_site
    if args.netlify_token:
        os.environ["NETLIFY_ACCESS_TOKEN"] = args.netlify_token
    
    # Validate environment
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OpenAI API key not provided. Set OPENAI_API_KEY or use --openai-key")
        return
    
    if not os.getenv("NETLIFY_SITE_ID"):
        logger.error("Netlify site ID not provided. Set NETLIFY_SITE_ID or use --netlify-site")
        return
    
    if not os.getenv("NETLIFY_ACCESS_TOKEN"):
        logger.error("Netlify access token not provided. Set NETLIFY_ACCESS_TOKEN or use --netlify-token")
        return
    
    # Create the ambient generator
    generator = create_ambient_pdf_generator(
        latitude=args.latitude,
        longitude=args.longitude,
        regeneration_hours=args.interval
    )
    
    if args.once:
        # Run once for testing
        logger.info("Running PDF generation once...")
        result = generator.run_once()
        logger.info(f"PDF generated: {result['public_url']}")
    else:
        # Run continuously
        logger.info(f"Starting ambient PDF generator...")
        logger.info(f"Latitude: {args.latitude}, Longitude: {args.longitude}")
        logger.info(f"Regeneration interval: {args.interval} hours")
        
        try:
            asyncio.run(generator.run_ambient())
        except KeyboardInterrupt:
            logger.info("Ambient generator stopped by user")


if __name__ == "__main__":
    main()