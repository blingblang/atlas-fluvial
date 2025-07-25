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
# Use fixed scale map generator - ALWAYS 1:375,000
from .fixed_scale_map import create_map_image as create_configured_map
from .netlify_uploader import upload_to_netlify


@tool
def generate_map(map_id: int = 1) -> str:
    """Generate a map image for the specified map ID.
    
    Args:
        map_id: The ID of the map to generate (1-53)
        
    Returns:
        Path to the generated map image
    """
    output_path = tempfile.mktemp(suffix='.png')
    return create_configured_map(map_id, output_path)


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
def upload_pdf_to_netlify(pdf_path: str, map_id: int = None) -> str:
    """Upload PDF to Netlify CDN.
    
    Args:
        pdf_path: Path to the PDF file
        map_id: Optional map ID for consistent naming (Map 1 gets consistent URL)
        
    Returns:
        Public URL of the uploaded PDF
    """
    return upload_to_netlify(pdf_path, map_id=map_id)


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
            1. Generate a map using the specified map ID from the configuration
            2. Create a PDF with two pages:
               - Page 1: Map page with the configured name
               - Page 2: Culture page with 6 sections (2x3 grid) and today's date
            3. Upload the PDF to Netlify CDN - when uploading, pass the map_id to ensure Map 1 gets a consistent URL
            
            Always follow this sequence: generate map -> create PDF -> upload to Netlify.
            When calling upload_pdf_to_netlify, always include the map_id parameter.
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
    
    def generate_pdf(self, map_id: int = 1) -> Dict[str, Any]:
        """Generate PDF with map and upload to Netlify.
        
        Args:
            map_id: The ID of the map to generate (1-53)
            
        Returns:
            Dictionary with generation results including the public URL
        """
        input_message = f"""Generate a PDF for Map ID {map_id}.
        
        Use the configuration from the JSON file to generate the appropriate map.
        The map will be centered at the configured coordinates with the specified scale and rotation.
        """
        
        result = self.executor.invoke({
            "input": input_message,
            "chat_history": []
        })
        
        return {
            "public_url": result["output"],
            "generated_at": datetime.now().isoformat(),
            "map_id": map_id
        }


def create_pdf_agent(openai_api_key: Optional[str] = None) -> PDFGeneratorAgent:
    """Create a PDF generator agent instance."""
    return PDFGeneratorAgent(openai_api_key)