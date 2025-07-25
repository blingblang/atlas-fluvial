"""LangChain agent for PDF generation."""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime
import tempfile
from pathlib import Path

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from .pdf_creator import create_pdf_with_map
# Use simple map generator by default to avoid Selenium/Folium issues
from .simple_map_generator import create_map_image
from .netlify_uploader import upload_to_netlify


@tool
def generate_map(latitude: float, longitude: float) -> str:
    """Generate a map image from NW corner coordinates.
    
    Args:
        latitude: Northwest corner latitude
        longitude: Northwest corner longitude
        
    Returns:
        Path to the generated map image
    """
    output_path = tempfile.mktemp(suffix='.png')
    return create_map_image(latitude, longitude, output_path)


@tool
def create_pdf(map_image_path: str) -> str:
    """Create a PDF with map and culture pages.
    
    Args:
        map_image_path: Path to the map image
        
    Returns:
        Path to the generated PDF
    """
    output_path = tempfile.mktemp(suffix='.pdf')
    return create_pdf_with_map(map_image_path, output_path)


@tool
def upload_pdf_to_netlify(pdf_path: str) -> str:
    """Upload PDF to Netlify CDN.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Public URL of the uploaded PDF
    """
    return upload_to_netlify(pdf_path)


class PDFGeneratorAgent:
    """Agent for generating and uploading PDFs with maps."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the PDF generator agent.
        
        Args:
            openai_api_key: OpenAI API key (optional if set in environment)
        """
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
        )
        
        self.tools = [generate_map, create_pdf, upload_pdf_to_netlify]
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a PDF generation agent that creates documents with maps and cultural information.
            
            Your task is to:
            1. Generate a map using OpenStreetMap data from the given NW corner coordinates
            2. Create a PDF with two pages:
               - Page 1: Map page labeled "Map 1"
               - Page 2: Culture page with 6 sections (2x3 grid) and today's date
            3. Upload the PDF to Netlify CDN
            
            Always follow this sequence: generate map -> create PDF -> upload to Netlify.
            Return the public URL of the uploaded PDF.
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True
        )
    
    def generate_pdf(self, nw_latitude: float, nw_longitude: float) -> Dict[str, Any]:
        """Generate PDF with map and upload to Netlify.
        
        Args:
            nw_latitude: Northwest corner latitude
            nw_longitude: Northwest corner longitude
            
        Returns:
            Dictionary with generation results including the public URL
        """
        input_message = f"""Generate a PDF with a map starting from NW corner at:
        Latitude: {nw_latitude}
        Longitude: {nw_longitude}
        
        The map should be at scale 1:375,000 and fit an A4 page.
        Include waterways and locks if available in the map data.
        """
        
        result = self.executor.invoke({
            "input": input_message,
            "chat_history": []
        })
        
        return {
            "public_url": result["output"],
            "generated_at": datetime.now().isoformat(),
            "coordinates": {
                "nw_latitude": nw_latitude,
                "nw_longitude": nw_longitude
            }
        }


def create_pdf_agent(openai_api_key: Optional[str] = None) -> PDFGeneratorAgent:
    """Create a PDF generator agent instance."""
    return PDFGeneratorAgent(openai_api_key)