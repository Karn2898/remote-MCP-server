try:
    from fastmcp import FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP
import random
import json

mcp=FastMCP("simple calculator server")

@mcp.tool()
def add(a:int , b: int):
    """Add two numbers"""
    return a + b
@mcp.tool()
def random_number(min:int=1, max:int=100):
    """Generate a random number between min and max"""
    return random.randint(min, max)
@mcp.resource("info://server")
def server_info():
    info={
        "name":"calculator",
        "version":"1.0.0",
        "description":"A simple calculator server that can add numbers and generate random numbers.",
        "tools":["add","random_number"],
        "author":"Tamaghna "
        
    }
    return json.dumps(info, indent=2)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
    