import unittest
import asyncio
from fastmcp.client import Client
from fastmcp.client.transports import FastMCPTransport
from goCodeMcpServer.go_mcp_server import GoCodeRunServer


class TestGoCodeRunServer(unittest.TestCase):
    def setUp(self):
        """Set up a FastMCP server with go_code_run tool."""
        self.go_server = GoCodeRunServer()
        
        # Create client with FastMCPTransport
        transport = FastMCPTransport(self.go_server.server)
        self.client = Client(transport)
    
    async def _run_go_code_test(self, go_code: str, included_expected_str:str):
        """Helper method to run Go code test with a callback to check results."""
        async with self.client:
            # Call the run_go_code tool with Go code parameter
            result = await self.client.call_tool("run_go_code", {"code": go_code})
            self.assertEqual(len(result), 1)
            
            # Use the callback to check the result
            self.assertIn(included_expected_str, result[0].text)

    def test_list_tools(self):
        """Test listing available tools."""
        async def run_test():
            async with self.client:
                tools = await self.client.list_tools()
                self.assertEqual(len(tools), 1)
                self.assertEqual(tools[0].name, "run_go_code")
        
        asyncio.run(run_test())

    def test_go_hello_world(self):
        """Test basic Hello World Go program."""
        go_code = '''package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}'''
        asyncio.run(self._run_go_code_test(go_code, "Hello, World!"))

    def test_go_addition_function(self):
        """Test Go program with addition function."""
        go_code = '''package main

import "fmt"

func add(a, b int) int {
    return a + b
}

func main() {
    result := add(2, 4)
    fmt.Printf("Result: %d\\n", result)
}'''
        
        asyncio.run(self._run_go_code_test(go_code, "Result: 6"))

if __name__ == "__main__":
    unittest.main()
