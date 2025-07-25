"""LangGraph implementation for ambient PDF generation."""

import os
import asyncio
from typing import Dict, Any, Optional, TypedDict, Annotated, Sequence
from datetime import datetime, timedelta
import logging
from pathlib import Path

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from .agent import generate_map, create_pdf, upload_pdf_to_netlify

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFGeneratorState(TypedDict):
    """State for PDF generation workflow."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    latitude: float
    longitude: float
    map_path: Optional[str]
    pdf_path: Optional[str]
    public_url: Optional[str]
    last_generated: Optional[datetime]
    generation_count: int


class AmbientPDFGenerator:
    """Ambient agent that regularly regenerates PDFs."""
    
    def __init__(self, 
                 nw_latitude: float,
                 nw_longitude: float,
                 openai_api_key: Optional[str] = None,
                 regeneration_interval_hours: int = 24):
        """Initialize the ambient PDF generator.
        
        Args:
            nw_latitude: Northwest corner latitude
            nw_longitude: Northwest corner longitude
            openai_api_key: OpenAI API key
            regeneration_interval_hours: Hours between regenerations
        """
        self.nw_latitude = nw_latitude
        self.nw_longitude = nw_longitude
        self.regeneration_interval = timedelta(hours=regeneration_interval_hours)
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0,
            api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
        )
        
        # Bind tools to LLM
        self.tools = [generate_map, create_pdf, upload_pdf_to_netlify]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create the graph
        self.graph = self._create_graph()
        self.memory = MemorySaver()
        self.app = self.graph.compile(checkpointer=self.memory)
    
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow."""
        # Define the graph
        workflow = StateGraph(PDFGeneratorState)
        
        # Add nodes
        workflow.add_node("plan", self._plan_generation)
        workflow.add_node("generate", self._call_model)
        workflow.add_node("tools", ToolNode(self.tools))
        workflow.add_node("check_completion", self._check_completion)
        
        # Set entry point
        workflow.set_entry_point("plan")
        
        # Add edges
        workflow.add_edge("plan", "generate")
        workflow.add_conditional_edges(
            "generate",
            self._should_use_tools,
            {
                "tools": "tools",
                "check": "check_completion"
            }
        )
        workflow.add_edge("tools", "generate")
        workflow.add_conditional_edges(
            "check_completion",
            self._is_complete,
            {
                "complete": END,
                "continue": "generate"
            }
        )
        
        return workflow
    
    def _plan_generation(self, state: PDFGeneratorState) -> Dict[str, Any]:
        """Plan the PDF generation process."""
        logger.info(f"Planning PDF generation #{state.get('generation_count', 0) + 1}")
        
        # Check if regeneration is needed
        last_generated = state.get("last_generated")
        if last_generated and datetime.now() - last_generated < self.regeneration_interval:
            logger.info("Skipping generation - not enough time has passed")
            return state
        
        # Create planning message
        plan_message = HumanMessage(content=f"""Generate a new PDF with the following requirements:
        1. Create a map from NW corner at Latitude: {state['latitude']}, Longitude: {state['longitude']}
        2. The map should be at scale 1:375,000 and fit an A4 page
        3. Create a PDF with the map on page 1 (labeled "Map 1") and culture page on page 2
        4. Upload the PDF to Netlify CDN
        5. Return the public URL
        
        This is generation #{state.get('generation_count', 0) + 1}.
        """)
        
        return {
            "messages": [plan_message],
            "generation_count": state.get("generation_count", 0) + 1
        }
    
    def _call_model(self, state: PDFGeneratorState) -> Dict[str, Any]:
        """Call the LLM to decide next action."""
        response = self.llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    
    def _should_use_tools(self, state: PDFGeneratorState) -> str:
        """Determine if tools should be used."""
        last_message = state["messages"][-1]
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        return "check"
    
    def _check_completion(self, state: PDFGeneratorState) -> Dict[str, Any]:
        """Check if PDF generation is complete."""
        # Look for public URL in messages
        for message in reversed(state["messages"]):
            if isinstance(message, ToolMessage):
                content = str(message.content)
                if "https://" in content and ".netlify.app/" in content:
                    state["public_url"] = content
                    state["last_generated"] = datetime.now()
                    logger.info(f"PDF generated successfully: {content}")
                    break
        
        return state
    
    def _is_complete(self, state: PDFGeneratorState) -> str:
        """Check if the workflow is complete."""
        if state.get("public_url") and state.get("last_generated"):
            recent_generation = datetime.now() - state["last_generated"] < timedelta(minutes=5)
            if recent_generation:
                return "complete"
        return "continue"
    
    async def run_ambient(self):
        """Run the ambient PDF generator continuously."""
        thread_id = "pdf-generator-thread"
        
        while True:
            try:
                logger.info("Starting PDF generation cycle...")
                
                # Run the graph
                config = {"configurable": {"thread_id": thread_id}}
                initial_state = {
                    "messages": [],
                    "latitude": self.nw_latitude,
                    "longitude": self.nw_longitude,
                    "generation_count": 0,
                    "map_path": None,
                    "pdf_path": None,
                    "public_url": None,
                    "last_generated": None
                }
                
                # Get current state or use initial
                current_state = self.app.get_state(config)
                if current_state.values:
                    initial_state.update(current_state.values)
                
                # Run the generation
                result = await self.app.ainvoke(initial_state, config, {"recursion_limit": 50})
                
                logger.info(f"Generation complete. URL: {result.get('public_url')}")
                
                # Wait for next cycle
                await asyncio.sleep(self.regeneration_interval.total_seconds())
                
            except Exception as e:
                logger.error(f"Error in PDF generation cycle: {e}")
                # Wait before retrying
                await asyncio.sleep(300)  # 5 minutes
    
    def run_once(self) -> Dict[str, Any]:
        """Run the PDF generator once (for testing)."""
        thread_id = "pdf-generator-test"
        config = {"configurable": {"thread_id": thread_id}}
        
        initial_state = {
            "messages": [],
            "latitude": self.nw_latitude,
            "longitude": self.nw_longitude,
            "generation_count": 0,
            "map_path": None,
            "pdf_path": None,
            "public_url": None,
            "last_generated": None
        }
        
        result = self.app.invoke(initial_state, config, {"recursion_limit": 50})
        return {
            "public_url": result.get("public_url"),
            "generated_at": result.get("last_generated"),
            "generation_count": result.get("generation_count")
        }


def create_ambient_pdf_generator(
    latitude: float,
    longitude: float,
    openai_api_key: Optional[str] = None,
    regeneration_hours: int = 24
) -> AmbientPDFGenerator:
    """Create an ambient PDF generator.
    
    Args:
        latitude: Northwest corner latitude
        longitude: Northwest corner longitude
        openai_api_key: OpenAI API key
        regeneration_hours: Hours between regenerations
        
    Returns:
        Configured ambient PDF generator
    """
    return AmbientPDFGenerator(
        nw_latitude=latitude,
        nw_longitude=longitude,
        openai_api_key=openai_api_key,
        regeneration_interval_hours=regeneration_hours
    )