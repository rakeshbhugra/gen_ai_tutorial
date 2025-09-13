import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

mcp_server_url = "http://localhost:8000/mcp"

async def main():
    async with streamablehttp_client(f"{mcp_server_url}") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()
            
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")

if __name__ == "__main__":
    print("Connecting to MCP server...")
    asyncio.run(main())
    print("Connection closed.")