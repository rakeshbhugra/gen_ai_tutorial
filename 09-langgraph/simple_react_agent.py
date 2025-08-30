from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

load_dotenv()

# Define the state with proper message handling
class MessagesState(TypedDict):
    messages: Annotated[List, add_messages]

# Define tool using LangChain decorator
@tool
def sum_numbers(a: float, b: float) -> float:
    """Add two numbers together and return the sum"""
    return a + b

# Define the reasoner node
def reasoner(state: MessagesState):
    """The reasoning node that decides what to do next"""
    from langchain_openai import ChatOpenAI
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools([sum_numbers])
    
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Create the graph
builder = StateGraph(MessagesState)

# Add nodes
builder.add_node("reasoner", reasoner)
builder.add_node("tools", ToolNode([sum_numbers]))

# Add edges
builder.add_edge(START, "reasoner")
builder.add_conditional_edges(
    "reasoner",
    tools_condition,
    {"tools": "tools", "__end__": "__end__"}
)
builder.add_edge("tools", "reasoner")

# Compile the graph
react_graph = builder.compile()

# Test the agent
if __name__ == "__main__":
    # Test with a simple math question
    result = react_graph.invoke({
        "messages": [HumanMessage(content="What is 25 + 17?")]
    })
    
    print("Agent conversation:")
    for message in result["messages"]:
        if hasattr(message, 'type'):
            print(f"{message.type}: {message.content}")
        else:
            print(f"message: {message}")