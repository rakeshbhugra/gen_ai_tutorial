from langgraph.graph import START, END, StateGraph
from pydantic import BaseModel
import json

# State
class State(BaseModel):
    messages: list[dict]
    search_results: str = ""

# Node functions
def chatbot_node(state: State):
    print("Chatbot node processing...")
    return state

def internet_search_node(state: State):
    print("Search node processing...")
    # mock search results
    state.search_results = "Mock search results for query."
    return state

# tool routing function
def route_by_tool(state: State):
    print("Routing based on tool...")
    last_user_message = state.messages[-1]["content"].lower()
    if "search" in last_user_message:
        return "search"
    else:
        return END

# Graph visualization
def visualize_graph(graph, name):
    try:
        png_data = graph.get_graph(xray=True).draw_mermaid_png()
        with open(name, "wb") as f:
            f.write(png_data)
        print(f"Graph diagram saved as '{name}'")
    except Exception as e:
        print(f"Could not generate graph image: {e}")

# Build graph
builder = StateGraph(State)
# adding nodes
builder.add_node("chatbot", chatbot_node)
builder.add_node("search", internet_search_node)

# adding edges
builder.add_edge(START, "chatbot")
builder.add_conditional_edges(
    "chatbot",
    route_by_tool,
    {
        "search": "search",
        END: END
    }
)

# compile
graph = builder.compile()

# visualize (optional)
visualize_graph(graph, name="internet_search_react_agent_graph.png")


# Run graph
# initiate state object

query = "search for me information about LangGraph and its use cases."
init_messages = [
    {"role": "user", "content": query}
]

init_state = State(messages=init_messages)

final_state = graph.invoke(init_state)
# print("Final state:", final_state)
print("Pretty print:", json.dumps(final_state, indent=2))