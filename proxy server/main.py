from fastmcp import FastMCP
import os


mcp = FastMCP.as_proxy(
    "https://splendid-gold-dingo.fastmcp.app/mcp",
    name="Nitish Server Proxy"
)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))