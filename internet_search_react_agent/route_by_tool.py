from state import State
from langgraph.graph import END

def route_by_tool(state: State):
    print("Routing based on tool...")
    if state.next_node == "search":
        return "search"
    else:
        return END