# Atlas Fluvial Observability Stack

This directory contains the Prometheus and Grafana observability stack for the Atlas Fluvial project, mirrored from the super-spork implementation.

## Architecture

The observability stack includes:
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **Node Exporter**: System metrics collection
- **Pushgateway**: For batch job metrics
- **Alertmanager**: Alert routing and management

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python application with prometheus-client library (for metrics instrumentation)

### Starting the Stack

1. Start all observability services:
```bash
cd observability
docker-compose up -d
```

2. Access the services:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/atlasfluvial2024)
- Pushgateway: http://localhost:9091
- Alertmanager: http://localhost:9093

### Stopping the Stack
```bash
docker-compose down
```

## Application Instrumentation

### Python Application Metrics

Install the prometheus client:
```bash
pip install prometheus-client
```

Example instrumentation for LangGraph agents:

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Metrics definitions
agent_requests = Counter('agent_requests_total', 'Total agent requests', ['agent_type', 'status'])
agent_duration = Histogram('agent_duration_seconds', 'Agent processing duration', ['agent_type'])
active_agents = Gauge('active_agents', 'Number of active agents')
langgraph_memory = Gauge('langgraph_memory_usage_bytes', 'LangGraph memory usage')

# Start metrics server on port 8000
start_http_server(8000)

# Example usage in your agent code
def process_agent_request(agent_type, request):
    active_agents.inc()
    start_time = time.time()

    try:
        # Your agent processing logic here
        result = run_agent(request)
        agent_requests.labels(agent_type=agent_type, status='success').inc()
        return result
    except Exception as e:
        agent_requests.labels(agent_type=agent_type, status='error').inc()
        raise
    finally:
        duration = time.time() - start_time
        agent_duration.labels(agent_type=agent_type).observe(duration)
        active_agents.dec()
```

### Custom Metrics for Atlas Fluvial

Add specific metrics for map generation and waterway analysis:

```python
from prometheus_client import Counter, Histogram, Summary

# Map generation metrics
map_generations = Counter('map_generations_total', 'Total map generations', ['region', 'status'])
map_generation_time = Histogram('map_generation_seconds', 'Map generation time', ['region'])
osm_api_calls = Counter('osm_api_calls_total', 'OpenStreetMap API calls', ['endpoint'])
waterway_analysis_duration = Summary('waterway_analysis_duration_seconds', 'Waterway analysis duration')

# PDF generation metrics
pdf_generations = Counter('pdf_generations_total', 'PDF generations', ['type'])
pdf_size_bytes = Histogram('pdf_size_bytes', 'Generated PDF size in bytes')
```

## Configuration

### Prometheus Configuration

The main configuration file is `prometheus/prometheus.yml`. It defines:
- Scrape intervals and targets
- Alert rules location
- Alertmanager configuration

Key scrape targets:
- `atlas-fluvial-app`: Main Python application (port 8000)
- `langgraph-agents`: LangGraph server metrics (port 8123)
- System metrics via node-exporter
- Prometheus and Grafana self-monitoring

### Grafana Configuration

Grafana is automatically configured with:
- Prometheus as the default datasource
- Pre-configured dashboards for system and application monitoring
- Custom Atlas Fluvial dashboards (to be created)

### Alert Rules

Alert rules are defined in `prometheus/alerts.yml` and include:
- Application health checks
- Agent-specific alerts (processing timeouts, memory usage)
- System resource alerts (CPU, memory, disk)
- SLO violations

## Dashboards

Two pre-configured dashboards are included:
1. **System Monitoring**: CPU, memory, disk, network metrics
2. **Application Performance**: Request rates, error rates, response times

### Creating Custom Dashboards

1. Access Grafana at http://localhost:3001
2. Create new dashboard
3. Add panels with Prometheus queries
4. Save and export as JSON to `grafana/dashboards/`

Example queries for Atlas Fluvial:
```promql
# Map generation rate
rate(map_generations_total[5m])

# Average map generation time by region
avg(map_generation_seconds) by (region)

# Agent processing P95 latency
histogram_quantile(0.95, rate(agent_duration_seconds_bucket[5m]))

# Active agents over time
active_agents
```

## Alerting

### Configure Alert Notifications

Edit `prometheus/alertmanager.yml` to add notification channels:

```yaml
receivers:
  - name: 'critical'
    webhook_configs:
      - url: 'http://your-webhook-url'
    email_configs:
      - to: 'alerts@example.com'
        from: 'prometheus@atlas-fluvial.com'
```

## Monitoring Best Practices

1. **Instrument key business metrics**: Map generations, waterway analyses, PDF exports
2. **Set up SLIs/SLOs**: Define service level indicators and objectives
3. **Create runbooks**: Document responses to common alerts
4. **Regular review**: Review metrics and adjust alerting thresholds
5. **Capacity planning**: Use metrics for resource planning

## Troubleshooting

### Services not starting
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs prometheus
docker-compose logs grafana
```

### Metrics not appearing
1. Verify application is exposing metrics endpoint
2. Check Prometheus targets: http://localhost:9090/targets
3. Ensure network connectivity between containers

### High memory usage
1. Adjust Prometheus retention: `--storage.tsdb.retention.time`
2. Reduce scrape frequency in prometheus.yml
3. Optimize metric cardinality (reduce label combinations)

## Development

### Adding New Metrics
1. Instrument your code with prometheus-client
2. Add scrape configuration to prometheus.yml
3. Create/update Grafana dashboards
4. Define relevant alerts

### Testing Alerts
```bash
# Send test metric to Pushgateway
echo "test_metric 42" | curl --data-binary @- http://localhost:9091/metrics/job/test

# Check alert status
curl http://localhost:9090/api/v1/alerts
```

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [prometheus-client Python](https://github.com/prometheus/client_python)
- [Best Practices for Metrics](https://prometheus.io/docs/practices/naming/)