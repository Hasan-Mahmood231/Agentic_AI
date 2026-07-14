import sys
from fastmcp import FastMCP

# 1. Initialize the MCP Server
mcp = FastMCP("Screen Output Server")

# 2. Define the tool that will show output on the screen
@mcp.tool()
def print_to_screen(text_to_print: str) -> str:
    """Prints incoming text directly to the server terminal console screen."""
    
    # We use file=sys.stderr so it prints directly to your screen 
    # without breaking the background data communication with the client.
    print(f"\n[SERVER SCREEN LOG]: {text_to_print}\n", file=sys.stderr)
    
    return f"Successfully displayed on server screen: '{text_to_print}'"

if __name__ == "__main__":
    # 3. Start the server using standard input/output (stdio)
    mcp.run(transport="stdio")