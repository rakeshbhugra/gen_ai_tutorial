from langgraph.graph import START, END, StateGraph
from typing import TypedDict, List
from dotenv import load_dotenv
import json
import litellm

load_dotenv()

# Define the state - just a simple list of message dicts
class MessagesState(TypedDict):
    messages: List[dict]

# Define tool functions (from the 07-tool-calling example)
def sum_numbers(a: float, b: float) -> float:
    """Add two numbers together and return the sum"""
    return a + b

def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together and return the product"""
    return a * b

# LiteLLM tool definitions
AVAILABLE_TOOLS = [
    {"type": "function", "function": litellm.utils.function_to_dict(sum_numbers)},
    {"type": "function", "function": litellm.utils.function_to_dict(multiply_numbers)},
]

# Function mapping for execution
FUNCTION_MAP = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
}

def execute_function_call(function_name: str, arguments: dict):
    """Execute a function call with given arguments."""
    if function_name not in FUNCTION_MAP:
        raise ValueError(f"Unknown function: {function_name}")
    
    try:
        return FUNCTION_MAP[function_name](**arguments)
    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"

# Define the reasoner node using LiteLLM
def reasoner(state: MessagesState):
    """The reasoning node that decides what to do next using LiteLLM"""
    # Call LiteLLM with tools directly - no conversion needed!
    response = litellm.completion(
        model="gpt-4o-mini",
        messages=state["messages"],
        tools=AVAILABLE_TOOLS,
        tool_choice="auto",
    )
    
    response_message = response.choices[0].message
    
    # Create message dict in LiteLLM format
    if response_message.tool_calls:
        ai_message = {
            "role": "assistant",
            "content": response_message.content or "",
            "tool_calls": response_message.tool_calls
        }
    else:
        ai_message = {
            "role": "assistant", 
            "content": response_message.content
        }
    
    return {"messages": state["messages"] + [ai_message]}

# Define the tools node
def tools_node(state: MessagesState):
    """Execute tool calls and return results"""
    last_message = state["messages"][-1]
    new_messages = []
    
    if last_message.get("tool_calls"):
        for tool_call in last_message["tool_calls"]:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"Calling function: {function_name} with args: {function_args}")
            
            # Execute the function
            try:
                result = execute_function_call(function_name, function_args)
                new_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
            except Exception as e:
                new_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Error: {str(e)}"
                })
    
    return {"messages": state["messages"] + new_messages}

# Simple condition function to check if we need tools
def should_continue(state: MessagesState):
    """Determine if we should continue to tools or end"""
    last_message = state["messages"][-1]
    if last_message.get("tool_calls"):
        return "tools"
    else:
        return "__end__"

# Create the graph
builder = StateGraph(MessagesState)

# Add nodes
builder.add_node("reasoner", reasoner)
builder.add_node("tools", tools_node)

# Add edges
builder.add_edge(START, "reasoner")
builder.add_conditional_edges(
    "reasoner",
    should_continue,
    {"tools": "tools", "__end__": END}
)
builder.add_edge("tools", "reasoner")

# Compile the graph
react_graph = builder.compile()

# Generate and save graph diagram
try:
    # Save the image to file
    png_data = react_graph.get_graph(xray=True).draw_mermaid_png()
    with open("react_agent_graph.png", "wb") as f:
        f.write(png_data)
    print("Graph diagram saved as 'react_agent_graph.png'")
    
except Exception as e:
    print(f"Could not generate graph image: {e}")

# Test the agent
if __name__ == "__main__":
    print("=== LangGraph ReAct Agent with LiteLLM ===\n")
    
    test_cases = [
        "What is 25 + 17?",
        "Calculate 8 multiplied by 12",
        "Add 15.5 and 23.7, then multiply the result by 2",
        "Hello, how are you today?"  # No tool needed
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case}")
        try:
            result = react_graph.invoke({
                "messages": [{"role": "user", "content": test_case}]
            })
            
            print("Agent conversation:")
            for message in result["messages"]:
                role = message.get("role", "unknown")
                content = message.get("content", "")
                print(f"{role}: {content}")
            print("-" * 50)
        except Exception as e:
            print(f"Error: {e}\n")