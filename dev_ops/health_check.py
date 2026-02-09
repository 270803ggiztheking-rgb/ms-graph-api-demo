"""
MCP Health Check Monitor
------------------------
Monitors the availability and latency of MCP servers.
"""

import time
import sys
import logging
from mcp_wrapper import MCPClient, MCPServer, NetworkError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - MONITOR - %(levelname)s - %(message)s')
logger = logging.getLogger("MCPHealth")

def check_server_health(client: MCPClient, server: MCPServer):
    start_time = time.time()
    try:
        # Simple ping-like operation
        if server == MCPServer.GITHUB:
            client.call_tool(server, "search_repositories", {"query": "health-check"})
        elif server == MCPServer.TESTSPRITE:
            client.call_tool(server, "testsprite_bootstrap", {"projectPath": ".", "localPort": 0, "type": "backend"})
        
        latency = (time.time() - start_time) * 1000
        logger.info(f"[{server.value.upper()}] Status: OK | Latency: {latency:.2f}ms")
        
        if latency > 2000:
            logger.warning(f"[{server.value.upper()}] High latency detected!")
            
        return True
    except Exception as e:
        logger.error(f"[{server.value.upper()}] Status: DOWN | Error: {str(e)}")
        return False

def main():
    logger.info("Starting MCP Health Check...")
    client = MCPClient()
    
    # Initialize Connections
    try:
        client.connect(MCPServer.GITHUB)
        client.connect(MCPServer.TESTSPRITE)
    except NetworkError:
        logger.critical("Failed to establish initial connections. Exiting.")
        sys.exit(1)

    # Run Checks
    github_ok = check_server_health(client, MCPServer.GITHUB)
    testsprite_ok = check_server_health(client, MCPServer.TESTSPRITE)

    if github_ok and testsprite_ok:
        logger.info("All systems operational.")
        sys.exit(0)
    else:
        logger.error("One or more systems are down.")
        sys.exit(1)

if __name__ == "__main__":
    main()
