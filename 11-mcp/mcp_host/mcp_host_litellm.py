import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import litellm
from litellm import experimental_mcp_client

mcp_server_url = "http://localhost:8000/mcp"

async def main():
    async with streamablehttp_client(f"{mcp_server_url}") as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

                # Check what the server actually offers
            tools_list = await session.list_tools()
            resources_list = await session.list_resources() 
            prompts_list = await session.list_prompts()
            
            print("Available Tools:", tools_list)
            print("Available Resources:", resources_list)  
            print("Available Prompts:", prompts_list)
            
            
            tools = await experimental_mcp_client.load_mcp_tools(session=session, format="openai")
            print("MCP Tools:", tools)

            messages = [{'role': 'user', 'content': 'What is 2 + 3?'}]
            llm_response = await litellm.acompletion(
                model="gpt-4.1-mini",
                messages=messages,
                tools=tools
            )

            print("llm_response:", json.dumps(llm_response, indent=2, default=str))

            openai_tool = llm_response["choices"][0]["message"]["tool_calls"][0]

            call_result = await experimental_mcp_client.call_openai_tool(
                session=session,
                openai_tool=openai_tool,
            )

            print("MCP Tool Call Result:", call_result)

            messages.append(llm_response["choices"][0]["message"])

            messages.append({
                "role": "tool",
                "content": str(call_result.content[0].text),
                "tool_call_id": openai_tool["id"],
            })

            print("final messages with tool result:\n", json.dumps(messages, indent=2, default=str))

            llm_response = await litellm.acompletion(
                model="gpt-4.1-mini",
                messages=messages,
                tools=tools
            )

            print("Final LLM Response:", json.dumps(llm_response, indent=2, default=str))

            

if __name__ == "__main__":
    print("Connecting to MCP server...")
    asyncio.run(main())
    print("Connection closed.")