# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import os
import asyncio
from langsmith import traceable
from dotenv import load_dotenv
load_dotenv()

model = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
        )
server_params = StdioServerParameters(
    command="python",
    args=["/Users/arjunts/Documents/GPT+LLM/2K25/documentation/docs_server.py"],
)


@traceable
async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke({"messages": "what is langchain"})
            print(agent_response)
    
if __name__ == "__main__":
    asyncio.run(main())