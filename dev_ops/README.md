# DevOps & MCP Integration

This directory contains the operational scripts and abstraction layers for integrating MCP (Model Context Protocol) servers into the development workflow.

## Files

- **`mcp_wrapper.py`**: The main abstraction layer (`MCPClient`) that standardizes calls to GitHub and TestSprite MCPs. Currently running in **Mock Mode** for demonstration.
- **`health_check.py`**: A monitoring script that pings the MCP servers to verify availability and latency.
- **`run_mcp_tests.py`**: A test suite to validate the integration logic.

## Usage

### Run Health Check
```bash
python dev_ops/health_check.py
```

### Run Integration Tests
```bash
python dev_ops/run_mcp_tests.py
```

## Configuration
See `mcp_wrapper.py` to toggle `_mock_mode` or configure server connection details.
