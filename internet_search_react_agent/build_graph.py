from internet_search_react_agent.state import State
from langgraph.graph import START, END, StateGraph
from internet_search_react_agent.nodes.chatbot_node import chatbot_node
from internet_search_react_agent.nodes.internet_search_node import internet_search_node
from internet_search_react_agent.route_by_tool import route_by_tool
from internet_search_react_agent.visualize_graph import visualize_graph

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

    # compile
    graph = builder.compile()

    # visualize (optional)
    visualize_graph(graph, name="internet_search_react_agent_graph.png")

    return graph
