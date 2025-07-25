# PDF Generator Agent

This LangChain/LangGraph agent generates PDFs with map and culture pages, then uploads them to Netlify CDN.

## Features

- **Map Generation**: Creates maps using OpenStreetMap data at 1:375,000 scale
- **PDF Creation**: Generates A4-sized PDFs with:
  - Page 1: Map labeled "Map 1" showing waterways and locks
  - Page 2: Culture page with 6 sections (2x3 grid) and update date
- **Netlify Upload**: Automatically uploads PDFs to Netlify CDN
- **Ambient Execution**: Runs continuously, regenerating PDFs at specified intervals

## Setup

1. Install dependencies:
```bash
uv sync --extra dev
# or
pip install -e .
```

2. Install Chrome/Chromium for map rendering (required by Selenium)

3. Set environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export NETLIFY_SITE_ID="your-netlify-site-id"
export NETLIFY_ACCESS_TOKEN="your-netlify-access-token"
```

## Usage

### Run Once (Testing)

```python
python example_pdf_generator.py
```

### Run Ambient Agent

```bash
# Run continuously (regenerates every 24 hours)
python -m src.pdf_generator.run_ambient_agent \
  --latitude 51.5074 \
  --longitude -0.1278

# Run once for testing
python -m src.pdf_generator.run_ambient_agent \
  --latitude 51.5074 \
  --longitude -0.1278 \
  --once

# Custom regeneration interval (e.g., every 6 hours)
python -m src.pdf_generator.run_ambient_agent \
  --latitude 51.5074 \
  --longitude -0.1278 \
  --interval 6
```

### Programmatic Usage

```python
from src.pdf_generator.langgraph_agent import create_ambient_pdf_generator

# Create generator
generator = create_ambient_pdf_generator(
    latitude=51.5074,
    longitude=-0.1278,
    regeneration_hours=24
)

# Run once
result = generator.run_once()
print(f"PDF URL: {result['public_url']}")

# Or run continuously
import asyncio
asyncio.run(generator.run_ambient())
```

## Architecture

1. **PDF Creator** (`pdf_creator.py`): ReportLab-based PDF generation
2. **Map Generator** (`map_generator.py`): Folium/Selenium map rendering
3. **Netlify Uploader** (`netlify_uploader.py`): API integration for CDN upload
4. **LangChain Agent** (`agent.py`): Orchestrates the workflow with tools
5. **LangGraph Agent** (`langgraph_agent.py`): Adds ambient execution capabilities

## Notes

- Coordinates should be provided as decimal degrees
- The map extends South and East from the NW corner
- PDF filenames include timestamps to prevent overwrites
- Chrome/Chromium must be installed for map rendering
- Netlify site must be configured to accept deployments