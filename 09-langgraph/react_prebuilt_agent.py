from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Define tools using LangChain decorator
@tool
def sum_numbers(a: float, b: float) -> float:
    """Add two numbers together and return the sum"""
    return a + b

@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together and return the product"""
    return a * b

# Create agent with the tools
agent = create_react_agent(
    model="openai:gpt-4.1-mini",
    tools=[sum_numbers, multiply_numbers],  # Pass both tool functions
    prompt="You are a helpful assistant"
)

# Test the agent
if __name__ == "__main__":
    result = agent.invoke({"messages": [("user", "What is 25 + 17? add 20 to the result")]})
    print("Agent response:")
    for message in result["messages"]:
        print(f"{message.type}: {message.content}")

