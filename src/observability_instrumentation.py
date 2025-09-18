"""Prometheus instrumentation for Atlas Fluvial application."""

from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
import time
import functools
from typing import Any, Callable
import psutil
import os

# Initialize metrics
# Agent metrics
agent_requests = Counter(
    'agent_requests_total',
    'Total agent requests',
    ['agent_type', 'status']
)

agent_duration = Histogram(
    'agent_duration_seconds',
    'Agent processing duration in seconds',
    ['agent_type'],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0)
)

active_agents = Gauge(
    'active_agents',
    'Number of currently active agents'
)

langgraph_memory = Gauge(
    'langgraph_memory_usage_bytes',
    'LangGraph memory usage in bytes'
)

# Map generation metrics
map_generations = Counter(
    'map_generations_total',
    'Total map generations',
    ['region', 'status']
)

map_generation_time = Histogram(
    'map_generation_seconds',
    'Map generation time in seconds',
    ['region'],
    buckets=(1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 120.0)
)

# OSM API metrics
osm_api_calls = Counter(
    'osm_api_calls_total',
    'OpenStreetMap API calls',
    ['endpoint', 'status']
)

osm_api_latency = Histogram(
    'osm_api_latency_seconds',
    'OSM API call latency',
    ['endpoint']
)

# Waterway analysis metrics
waterway_analysis_duration = Summary(
    'waterway_analysis_duration_seconds',
    'Waterway analysis duration'
)

waterways_processed = Counter(
    'waterways_processed_total',
    'Total waterways processed',
    ['waterway_type']
)

# PDF generation metrics
pdf_generations = Counter(
    'pdf_generations_total',
    'PDF generations',
    ['type', 'status']
)

pdf_size_bytes = Histogram(
    'pdf_size_bytes',
    'Generated PDF size in bytes',
    buckets=(1024, 10240, 102400, 1048576, 10485760)  # 1KB, 10KB, 100KB, 1MB, 10MB
)

# Email processing metrics
emails_processed = Counter(
    'emails_processed_total',
    'Emails processed',
    ['action', 'status']
)

email_processing_time = Histogram(
    'email_processing_seconds',
    'Email processing time',
    ['action']
)

# System metrics
process_memory_bytes = Gauge(
    'process_memory_bytes',
    'Process memory usage in bytes'
)


def start_metrics_server(port: int = 8000):
    """Start the Prometheus metrics HTTP server.

    Args:
        port: Port to serve metrics on (default: 8000)
    """
    start_http_server(port)
    print(f"Metrics server started on port {port}")
    # Start collecting system metrics
    update_system_metrics()


def update_system_metrics():
    """Update system-level metrics."""
    try:
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        process_memory_bytes.set(memory_info.rss)

        # Update LangGraph memory if available
        # This is a placeholder - replace with actual memory measurement
        langgraph_memory.set(memory_info.vms)
    except Exception as e:
        print(f"Error updating system metrics: {e}")


def track_agent_request(agent_type: str):
    """Decorator to track agent request metrics.

    Args:
        agent_type: Type of agent being tracked
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            active_agents.inc()
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                agent_requests.labels(agent_type=agent_type, status='success').inc()
                return result
            except Exception as e:
                agent_requests.labels(agent_type=agent_type, status='error').inc()
                raise
            finally:
                duration = time.time() - start_time
                agent_duration.labels(agent_type=agent_type).observe(duration)
                active_agents.dec()
                update_system_metrics()

        return wrapper
    return decorator


def track_map_generation(region: str):
    """Decorator to track map generation metrics.

    Args:
        region: Region being mapped
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                map_generations.labels(region=region, status='success').inc()
                return result
            except Exception as e:
                map_generations.labels(region=region, status='error').inc()
                raise
            finally:
                duration = time.time() - start_time
                map_generation_time.labels(region=region).observe(duration)

        return wrapper
    return decorator


def track_osm_api_call(endpoint: str):
    """Decorator to track OSM API calls.

    Args:
        endpoint: OSM API endpoint being called
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                osm_api_calls.labels(endpoint=endpoint, status='success').inc()
                return result
            except Exception as e:
                osm_api_calls.labels(endpoint=endpoint, status='error').inc()
                raise
            finally:
                duration = time.time() - start_time
                osm_api_latency.labels(endpoint=endpoint).observe(duration)

        return wrapper
    return decorator


def track_pdf_generation(pdf_type: str):
    """Decorator to track PDF generation metrics.

    Args:
        pdf_type: Type of PDF being generated
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                pdf_generations.labels(type=pdf_type, status='success').inc()

                # If result contains file path or bytes, track size
                if isinstance(result, bytes):
                    pdf_size_bytes.observe(len(result))
                elif isinstance(result, str) and os.path.exists(result):
                    pdf_size_bytes.observe(os.path.getsize(result))

                return result
            except Exception as e:
                pdf_generations.labels(type=pdf_type, status='error').inc()
                raise

        return wrapper
    return decorator


def track_email_processing(action: str):
    """Decorator to track email processing metrics.

    Args:
        action: Email action being performed (triage, draft, send, etc.)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                emails_processed.labels(action=action, status='success').inc()
                return result
            except Exception as e:
                emails_processed.labels(action=action, status='error').inc()
                raise
            finally:
                duration = time.time() - start_time
                email_processing_time.labels(action=action).observe(duration)

        return wrapper
    return decorator


# Example usage in your application
if __name__ == "__main__":
    # Start metrics server
    start_metrics_server(8000)

    # Example instrumented functions
    @track_agent_request("map_agent")
    def process_map_request(request_data):
        """Process a map generation request."""
        time.sleep(2)  # Simulate processing
        return {"status": "completed"}

    @track_map_generation("nantes")
    def generate_nantes_map():
        """Generate map for Nantes region."""
        time.sleep(3)  # Simulate map generation
        return "map.png"

    @track_osm_api_call("overpass")
    def fetch_osm_data(query):
        """Fetch data from OSM Overpass API."""
        time.sleep(1)  # Simulate API call
        return {"data": "osm_data"}

    @track_pdf_generation("map")
    def generate_pdf_map(map_data):
        """Generate PDF from map data."""
        time.sleep(2)  # Simulate PDF generation
        return b"PDF content here"  # Return bytes for size tracking

    # Test the instrumented functions
    print("Testing instrumented functions...")

    process_map_request({"region": "nantes"})
    generate_nantes_map()
    fetch_osm_data("waterways")
    pdf_content = generate_pdf_map({"map": "data"})

    print("Metrics are now available at http://localhost:8000")
    print("Press Ctrl+C to stop...")

    # Keep the server running
    try:
        while True:
            time.sleep(10)
            update_system_metrics()
    except KeyboardInterrupt:
        print("\nShutting down metrics server...")