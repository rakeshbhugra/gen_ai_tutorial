import asyncio
import json
from dotenv import load_dotenv
load_dotenv()

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

mcp_server_url = "http://localhost:8000/mcp"

def get_response(messages):
    return asyncio.run(get_bot_response(messages))

async def get_bot_response(messages):
    async with streamablehttp_client(f"{mcp_server_url}") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()
            
            tools = await load_mcp_tools(session=session)
            print("MCP Tools:", tools)

            # Supervisor
            agent = create_react_agent(
                model="openai:gpt-4.1-mini",
                tools=tools,
                prompt="You are a helpful assistant"
            )

            agent_response = await agent.ainvoke(
                {"messages": messages}
            )

            for m in agent_response["messages"]:
                m.pretty_print()

            # Return the last AI message content
            for message in reversed(agent_response["messages"]):
                if hasattr(message, 'content') and message.type == "ai":
                    return message.content

            return "No response generated"

if __name__ == "__main__":
    print("Connecting to MCP server...")
    # query = "What is the total, average, min and max amount due across all customers?"
    query = "Who is the top borrower?"
    # query = "Send email to manager@example.com that I am running late for the meeting."
    asyncio.run(get_bot_response(query))
    print("Connection closed.")