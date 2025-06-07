# mcp-example-go-code

a simple MCP server demo code for running go code in MCP way 

the go code is passed to the MCP server, which then executes it and returns the result.

## prerequisites

make sure you already have the following tools installed:
- [go](https://golang.org/doc/install/source)
- [python](https://www.python.org/downloads/)
    

## get started

```bash

# prerequisites
# verify golang and python are installed
go version
python3 --version

# 1. clone the repo

git clone github.com:extraintelligen/mcp-example-go-code.git 

# 2. change directory to the repo
cd mcp-example-go-code

# 3. create a virtual environment
python3 -m venv venv

# 4. activate the virtual environment
source venv/bin/activate

# 5. install uv for dependencies management
pip install uv

# 6. install the dependencies
uv install

```

