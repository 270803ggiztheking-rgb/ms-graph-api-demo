"""
MCP Integration Tests
---------------------
Validates the abstraction layer and mock integration logic.
"""

import unittest
from mcp_wrapper import MCPClient, MCPServer, ToolResult, ValidationError

class TestMCPWrapper(unittest.TestCase):
    
    def setUp(self):
        self.client = MCPClient()
        self.client.connect(MCPServer.GITHUB)
        self.client.connect(MCPServer.TESTSPRITE)

    def test_github_search(self):
        """Test GitHub search tool."""
        result = self.client.call_tool(MCPServer.GITHUB, "search_repositories", {"query": "test"})
        self.assertTrue(result.success)
        self.assertIn("items", result.data)

    def test_testsprite_plan(self):
        """Test TestSprite plan generation."""
        result = self.client.call_tool(MCPServer.TESTSPRITE, "testsprite_generate_backend_test_plan", 
                                      {"projectPath": "."})
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data.get("plan_id"))

    def test_validation_error(self):
        """Test error handling for missing parameters."""
        result = self.client.call_tool(MCPServer.GITHUB, "get_file_contents", {}) # Missing path
        self.assertFalse(result.success)
        self.assertIn("Missing path parameter", result.error)

    def test_high_level_workflow(self):
        """Test the high-level orchestration methods."""
        repo_data = self.client.sync_repo_state("my-repo")
        self.assertIsNotNone(repo_data)
        
        test_plan = self.client.run_test_suite(".")
        self.assertIsNotNone(test_plan)

if __name__ == '__main__':
    unittest.main()
