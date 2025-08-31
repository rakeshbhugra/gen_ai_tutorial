from internet_search_react_agent.state import State
from langgraph.graph import END

def route_by_tool(state: State):
    print("Routing based on tool...")
    last_user_message = state.messages[-1]["content"].lower()
    if "search" in last_user_message:
        return "search"
    else:
        return END