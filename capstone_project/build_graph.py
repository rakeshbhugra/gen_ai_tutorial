from langgraph.graph import StateGraph, END, START
from state import State
from nodes.email_classifier_node import email_classifier_node
from nodes.customer_support_agent_node import customer_support_agent_node
from nodes.customer_support_rag_node import customer_support_rag_node
from nodes.sales_agent_node import sales_agent_node
from nodes.sales_rag_node import sales_rag_node
from nodes.human_in_the_loop_node import human_in_the_loop_node
from nodes.send_email_node import send_email_node
from routing.route_by_classification import route_by_classification
from routing.route_by_tool import route_by_tool

def build_graph():
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

    return builder.compile()