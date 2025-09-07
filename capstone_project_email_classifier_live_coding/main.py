# create nodes
# create a graph
# create edges
# visualize the graph (optional)
# fill in the functions with mock logic to test the flow
# fill in the functions with actual logic


from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel


class State(BaseModel):
    messages: list[str] = []

# nodes

def classifier_node(state: State):
    print("Classifying email...")
    # mock classification logic
    return state

def customer_support_agent_node(state: State):
    print("Routing to Customer Support Agent...")
    # mock routing logic
    return state

def customer_support_rag_node(state: State):
    print("Routing to Customer Support RAG...")
    # mock routing logic
    return state

def sales_agent_node(state: State):
    print("Routing to Sales Agent...")
    # mock routing logic
    return state

def sales_rag_node(state: State):
    print("Routing to Sales Support RAG...")
    # mock routing logic
    return state

def human_in_the_loop_node(state: State):
    print("Routing to Human in the Loop...")
    # mock routing logic
    return state

def send_email_node(state: State):
    print("Sending email...")
    # mock sending logic
    return state


def route_by_classification(state: State):
    # mock routing logic based on classification
    return "customer_support_agent"  # or "sales_agent" or "human_in_the_loop"

def route_by_tool(state: State):
    return "RAG"

builder = StateGraph(State)

builder.add_node("classifier", classifier_node)
builder.add_node("customer_support_agent", customer_support_agent_node)
builder.add_node("customer_support_rag", customer_support_rag_node)
builder.add_node("sales_agent", sales_agent_node)
builder.add_node("sales_rag", sales_rag_node)
builder.add_node("human_in_the_loop", human_in_the_loop_node)
builder.add_node("send_email", send_email_node)


builder.add_edge(START, "classifier")
builder.add_conditional_edges(
    "classifier",
    route_by_classification,
    {
        "customer_support_agent": "customer_support_agent",
        "sales_agent": "sales_agent",
        "human_in_the_loop": "human_in_the_loop"
    }
)

builder.add_conditional_edges(
    "customer_support_agent",
    route_by_tool,
    {
        "customer_support_rag": "customer_support_rag",
        "send_email": "send_email"
    }
)

builder.add_edge("customer_support_rag", "customer_support_agent")

builder.add_conditional_edges(
    "sales_agent",
    route_by_tool,
    {
        "sales_rag": "sales_rag",
        "send_email": "send_email"
    }
)

builder.add_edge("sales_rag", "sales_agent")

builder.add_edge("human_in_the_loop", "send_email")

graph = builder.compile()


def visualize_graph(graph, name):
    try:
        png_data = graph.get_graph(xray=True).draw_mermaid_png()
        with open(name, "wb") as f:
            f.write(png_data)
        print(f"Graph diagram saved as '{name}'")
    except Exception as e:
        print(f"Could not generate graph image: {e}")

        
visualize_graph(graph, "email_classifier_graph.png")