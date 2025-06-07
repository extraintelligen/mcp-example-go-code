import subprocess
import os
import tempfile
import shutil
import argparse
from fastmcp.server.server import FastMCP


class GoCodeRunServer:
    """MCP Server for running Go code."""
    
    def __init__(self, name: str = "go-code-run-server"):
        self.server = FastMCP(name)
        self._setup_tools()
    
    def getServer(self):
        """Get the FastMCP server instance."""
        return self.server
    
    def _setup_tools(self):
        """Register the run_go_code tool with the server."""
        @self.server.tool()
        def run_go_code(code: str) -> str:
            """Executes or analyzes Go code and returns the result"""
            return self.run_go_code(code)
    
    def _validate_code(self, code: str) -> str:
        """Validate the Go code input."""
        MAX_CODE_LENGTH = 1024 * 1024  # 1MB limit
        
        if len(code) > MAX_CODE_LENGTH:
            return f"Error: Code too long. Maximum length is {MAX_CODE_LENGTH} characters."
        
        if not code.strip():
            return "Error: Empty code provided."
        
        return ""

    def _save_go_code(self, code: str, temp_dir: str) -> str:
        """Save Go code to main.go file in the temporary directory."""
        main_go_path = os.path.join(temp_dir, "main.go")
        with open(main_go_path, 'w') as f:
            f.write(code)
        return main_go_path

    def _build_go_code(self, temp_dir: str) -> tuple[bool, str]:
        """Build the Go code and return success status and error message if any."""
        build_result = subprocess.run(
            ["go", "build", "-o", "main", "main.go"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if build_result.returncode != 0:
            return False, f"Build Error:\n{build_result.stderr}"
        
        return True, ""

    def _run_go_binary(self, temp_dir: str) -> tuple[bool, str]:
        """Run the compiled Go binary and return success status and output/error."""
        run_result = subprocess.run(
            ["./main"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if run_result.returncode != 0:
            return False, f"Runtime Error:\n{run_result.stderr}"
        
        return True, f"Output:\n{run_result.stdout}"
    
    def run_go_code(self, code: str) -> str:
        """Main method to execute Go code and return the result."""
        # Validate input
        validation_error = self._validate_code(code)
        if validation_error:
            return validation_error
        
        # Create temporary directory for Go code execution
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Save code to file
            self._save_go_code(code, temp_dir)
            
            # Build the Go code
            build_success, build_message = self._build_go_code(temp_dir)
            if not build_success:
                return build_message
            
            # Run the compiled binary
            run_success, run_message = self._run_go_binary(temp_dir)
            return run_message
            
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out."
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Go Code Run MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()

    server = GoCodeRunServer()
    print(f"start running go code server on port {args.port} with SSE mode")
    server.getServer().run(transport="sse", host= "127.0.0.1", port=args.port, path = "/go")  # Use sse=True for Server-Sent Events mode
    print("Server stopped.")
