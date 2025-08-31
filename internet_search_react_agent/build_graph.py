from state import State
from langgraph.graph import START, END, StateGraph
from nodes.chatbot_node import chatbot_node
from nodes.internet_search_node import internet_search_node
from route_by_tool import route_by_tool
from visualize_graph import visualize_graph

def build_graph():
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
    builder.add_edge("search", "chatbot")

    # compile
    graph = builder.compile()

    # visualize (optional)
    visualize_graph(graph, name="internet_search_react_agent_graph.png")

    return graph
