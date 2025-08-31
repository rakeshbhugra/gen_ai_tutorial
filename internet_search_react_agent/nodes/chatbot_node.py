from state import State
from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import litellm
from langgraph.graph import END
import json

load_dotenv()

def search_internet_tool(query: str) -> str:
    """Simulate an internet search and return results.
    
    Parameters
    ----------
    query : str
        The search query string.
    
    Returns
    -------
    str
        Simulated search results.
    """
    # Simulate search results
    search = SerpAPIWrapper()
    result = search.run(query)
    return str(result)

# use function to dict
tools = [
    {"type": "function", "function": litellm.utils.function_to_dict(search_internet_tool)}
]

# function mapping
function_mapping = {
    "search_internet": search_internet_tool
}

def chatbot_node(state: State):
    print("Chatbot node processing...")
    response = litellm.completion(
        model="openai/gpt-4.1-mini",
        messages=state.messages,
        tool_choice="auto",
        tools=tools,
    )

    response_message = response.choices[0].message
    # print(f"Model response: {response_message}")

    if response_message.tool_calls:
        print("Model wants to call a tool...")
        print(f"Tool call: {response_message.tool_calls[0]}")
        state.messages.append(
            {
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": response_message.tool_calls
            }
        )
        state.next_node = "search"
        tool_call = response_message.tool_calls[0]
        state.tool_call_id = tool_call.id
        function_args = json.loads(tool_call.function.arguments)
        state.search_query = function_args.get("query")

    else:
        # just answer
        state.messages.append(
            {
                "role": "assistant",
                "content": response_message.content,
            }
        )
        state.next_node = END
        # state.tool_call_id = None
        # state.search_query = None
        # state.search_results = None
        print("Final answer generated.")
        print(f"AI: {response_message.content}")
        pass

    return state