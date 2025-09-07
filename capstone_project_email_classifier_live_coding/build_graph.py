from state import State
from langgraph.graph import StateGraph, START, END
from nodes import (
    classifier_node,
    customer_support_agent_node,
    customer_support_rag_node,
    sales_agent_node,
    sales_rag_node,
    human_in_the_loop_node,
    send_email_node
)

from routing_algos import (
    route_by_classification,
    route_by_tool
)

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