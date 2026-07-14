import os
import asyncio
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama

load_dotenv()

async def main():
    # 1. Define the server launch configuration
    mcp_config = {
        "my-screen-server": {
            "command": "python",
            "args": ["myServer.py"], # Must match your exact server filename
            "transport": "stdio"
        }
    }
    
    print("Starting client and launching the server process...")
    
    # 2. Use 'async with' to cleanly open and manage the background connection
    async with MultiServerMCPClient(mcp_config) as client:
        
        print("\n________________________________________________________COLLECTING TOOLS_________________________________________________________\n")
        # Automatically discover tools from the active session
        tools = await client.get_tools()
        print(tools, end="\n")
        print("________________________________________________________TOOLS COLLECTED_________________________________________________________\n")
        
        # 3. Initialize the local Ollama LLM brain
        model = ChatOllama(model="qwen2.5:3b")

        # 4. Bind discovered tools to the agent workflow
        agent = create_react_agent(model, tools)
        
        # 5. Execute the prompt
        user_prompt = "Please print the message 'Hello Hassan, MCP is working perfectly!' to the screen."
        print(f"Sending prompt to AI: '{user_prompt}'\n")
        
        # Run the agent loop
        response = await agent.ainvoke({"messages": [("user", user_prompt)]})
        print("Agent has finished execution.")

if __name__ == "__main__":
    asyncio.run(main())