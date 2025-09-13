import asyncio
import json
from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools


from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

mcp_server_url = "http://localhost:8931/mcp"

async def main():
    async with streamablehttp_client(f"{mcp_server_url}") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()
            
            tools = await load_mcp_tools(session=session)
            # print("MCP Tools:", tools)

            agent = create_react_agent(
                model="openai:gpt-4.1-mini",
                tools=tools,
                prompt="You are a helpful assistant"
            )

            agent_response = await agent.ainvoke(
                {"messages": "open google.com then search for langgraph mcp and summarise the page"}
            )

            for m in agent_response["messages"]:
                m.pretty_print()

if __name__ == "__main__":
    print("Connecting to MCP server...")
    asyncio.run(main())
    print("Connection closed.")