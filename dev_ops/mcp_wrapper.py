"""
MCP Wrapper - Abstraction Layer
-------------------------------
Standardizes interactions with GitHub and TestSprite MCP servers.
"""

import time
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MCPWrapper")

class MCPError(Exception):
    """Base class for MCP errors."""
    pass

class NetworkError(MCPError):
    """Connection failures."""
    pass

class AuthError(MCPError):
    """Authentication failures."""
    pass

class ValidationError(MCPError):
    """Invalid parameters."""
    pass

class BusinessLogicError(MCPError):
    """Operational failures."""
    pass

@dataclass
class ToolResult:
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class MCPServer(Enum):
    GITHUB = "github"
    TESTSPRITE = "testsprite"

class MCPClient:
    def __init__(self):
        self.connected_servers = {}
        self._mock_mode = True  # Enable mock mode since real MCP connection requires stdio/SSE setup

    def connect(self, server: MCPServer) -> bool:
        """Establishes connection to the specified MCP server."""
        try:
            logger.info(f"Connecting to {server.value} MCP server...")
            # Simulation of connection delay
            time.sleep(0.5) 
            
            # In a real implementation, this would establish stdio/SSE connection
            self.connected_servers[server] = True
            logger.info(f"Successfully connected to {server.value}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {server.value}: {str(e)}")
            raise NetworkError(f"Connection failed: {str(e)}")

    def call_tool(self, server: MCPServer, tool_name: str, params: Dict[str, Any]) -> ToolResult:
        """
        Generic method to call an MCP tool with retry logic.
        """
        if server not in self.connected_servers:
            raise NetworkError(f"Server {server.value} not connected")

        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Calling {tool_name} on {server.value} (Attempt {attempt+1})")
                
                # Validation Logic (Mock)
                if not tool_name:
                    raise ValidationError("Tool name cannot be empty")

                # Mock Execution Logic
                result = self._execute_mock_tool(server, tool_name, params)
                return result

            except ValidationError as e:
                # Don't retry validation errors
                logger.error(f"Validation error: {str(e)}")
                return ToolResult(success=False, error=str(e))
            except Exception as e:
                if attempt == max_retries - 1:
                    logger.error(f"Max retries reached for {tool_name}: {str(e)}")
                    return ToolResult(success=False, error=str(e))
                logger.warning(f"Retryable error: {str(e)}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff

        return ToolResult(success=False, error="Unknown error")

    def _execute_mock_tool(self, server: MCPServer, tool_name: str, params: Dict[str, Any]) -> ToolResult:
        """
        Simulates tool execution for testing purposes.
        """
        time.sleep(0.2) # Simulate latency

        if server == MCPServer.GITHUB:
            if tool_name == "search_repositories":
                return ToolResult(success=True, data={"items": [{"name": "ms-graph-api-demo"}]})
            elif tool_name == "get_file_contents":
                if "path" not in params:
                    raise ValidationError("Missing path parameter")
                return ToolResult(success=True, data={"content": "Mock file content"})
            
        elif server == MCPServer.TESTSPRITE:
            if tool_name == "testsprite_bootstrap":
                return ToolResult(success=True, data={"status": "ready"})
            elif tool_name == "testsprite_generate_backend_test_plan":
                return ToolResult(success=True, data={"plan_id": "plan-123", "tests": ["test_auth", "test_user"]})

        return ToolResult(success=True, data={"mock": "generic_response"})

    # --- High Level Abstractions ---

    def sync_repo_state(self, repo_name: str):
        """High-level workflow to sync repository state."""
        logger.info(f"Syncing state for {repo_name}")
        result = self.call_tool(MCPServer.GITHUB, "search_repositories", {"query": repo_name})
        if not result.success:
            raise BusinessLogicError(f"Repo sync failed: {result.error}")
        return result.data

    def run_test_suite(self, project_path: str):
        """High-level workflow to generate and run tests."""
        logger.info(f"Running test suite for {project_path}")
        
        # 1. Bootstrap
        bs_result = self.call_tool(MCPServer.TESTSPRITE, "testsprite_bootstrap", 
                                  {"projectPath": project_path, "localPort": 8000, "type": "backend"})
        if not bs_result.success:
            raise BusinessLogicError("Bootstrap failed")

        # 2. Generate Plan
        plan_result = self.call_tool(MCPServer.TESTSPRITE, "testsprite_generate_backend_test_plan", 
                                    {"projectPath": project_path})
        
        return plan_result.data
