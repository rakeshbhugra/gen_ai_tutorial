from langgraph.graph import StateGraph, END, START
from pydantic import BaseModel

# state
class State(BaseModel):
    messages: list[dict] = []

# nodes

# email classifier 
# customer support agent
# customer support rag
# sales agent
# sales rag
# human in the loop

def email_classifier_node(state: State):
    pass

def customer_support_agent_node(state: State):
    pass

def customer_support_rag_node(state: State):
    pass

def sales_agent_node(state: State):
    pass

def sales_rag_node(state: State):
    pass

def human_in_the_loop_node(state: State):
    pass

def send_email_node(state: State):
    pass

# route by classification
def route_by_classification(state: State):
    last_message = state.messages[-1]["content"].lower()
    if "support" in last_message:
        return "customer_support_agent"
    elif "sales" in last_message:
        return "sales_agent"
    else:
        return "human_in_the_loop"

def route_by_tool(state: State):
    last_user_message = state.messages[-1]["content"].lower()
    if "send_email" in last_user_message:
        return "send_email"
    else:
        return "RAG"

# graph
builder = StateGraph(State)

builder.add_node("email_classifier", email_classifier_node)
builder.add_node("customer_support_agent", customer_support_agent_node)
builder.add_node("customer_support_rag", customer_support_rag_node)
builder.add_node("sales_agent", sales_agent_node)
builder.add_node("sales_rag", sales_rag_node)
builder.add_node("human_in_the_loop", human_in_the_loop_node)
builder.add_node("send_email", send_email_node)

builder.add_edge(START, "email_classifier")
builder.add_conditional_edges(
    "email_classifier",
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
        "send_email": "send_email",
        "RAG": "customer_support_rag"
    }
    
)
builder.add_conditional_edges(
    "sales_agent",
    route_by_tool,
    {
        "send_email": "send_email",
        "RAG": "sales_rag"
    }
    
)
builder.add_edge("customer_support_rag", "customer_support_agent")
builder.add_edge("sales_rag", "sales_agent")
builder.add_edge("human_in_the_loop", "send_email")

# compile
graph = builder.compile()

# visualize (optional)
def visualize_graph(graph, name):
    try:
        png_data = graph.get_graph(xray=True).draw_mermaid_png()
        with open(name, "wb") as f:
            f.write(png_data)
        print(f"Graph diagram saved as '{name}'")
    except Exception as e:
        print(f"Could not generate graph image: {e}")

visualize_graph(graph, name="capstone_project_graph.png")
