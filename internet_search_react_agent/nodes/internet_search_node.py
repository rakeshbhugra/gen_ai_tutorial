from internet_search_react_agent.state import State
from nodes.chatbot_node import search_internet_tool
from dotenv import load_dotenv
load_dotenv()

def internet_search_node(state: State):
    print("Search node processing...")
    result = search_internet_tool(state.search_query)
    state.search_results = result
    state.messages.append({
        "role": "tool",
        "tool_call_id": state.tool_call_id,
        "content": result
    })
    return state