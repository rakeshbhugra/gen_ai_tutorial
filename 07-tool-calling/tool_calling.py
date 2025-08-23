"""
LiteLLM Tool Calling Implementation with Basic Sum Tool

This module demonstrates best practices for function calling with LiteLLM,
including:
- Proper function definition structure
- Tool choice configuration
- Function execution pattern
- Error handling
"""

import json
import litellm
from dotenv import load_dotenv

load_dotenv()

def sum_numbers(a: float, b: float) -> float:
    """Add two numbers together and return the sum
    
    Parameters
    ----------
    a : float
        The first number to add
    b : float
        The second number to add
    """
    return a + b

def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together and return the product
    
    Parameters
    ----------
    a : float
        The first number to multiply
    b : float
        The second number to multiply
    """
    return a * b

def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather for a specific location
    
    Parameters
    ----------
    location : str
        The city and state, e.g. San Francisco, CA
    unit : str {'celsius', 'fahrenheit'}
        The temperature unit to use
    """
    # Mock weather data
    temp = 72 if unit == "fahrenheit" else 22
    return json.dumps({
        "location": location,
        "temperature": temp,
        "unit": unit,
        "condition": "sunny"
    })

# Use function_to_dict - much cleaner than manual JSON schema!
AVAILABLE_TOOLS = [
    {"type": "function", "function": litellm.utils.function_to_dict(sum_numbers)},
    {"type": "function", "function": litellm.utils.function_to_dict(multiply_numbers)},
    {"type": "function", "function": litellm.utils.function_to_dict(get_current_weather)}
]

# Function mapping for execution
FUNCTION_MAP = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
    "get_current_weather": get_current_weather
}

def execute_function_call(function_name: str, arguments: dict):
    """
    Execute a function call with given arguments.
    
    Args:
        function_name (str): Name of the function to call
        arguments (dict): Arguments to pass to the function
        
    Returns:
        The result of the function call
    """
    if function_name not in FUNCTION_MAP:
        raise ValueError(f"Unknown function: {function_name}")
    
    try:
        return FUNCTION_MAP[function_name](**arguments)
    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"

def chat_with_tools(user_message: str, model: str = "gemini/gemini-2.5-flash-lite"):
    """
    Complete chat interaction with tool calling support.
    
    Args:
        user_message (str): The user's message
        model (str): The model to use for completion
        
    Returns:
        str: The final response from the model
    """
    # Check if model supports function calling
    if not litellm.supports_function_calling(model):
        print(f"Warning: {model} may not support function calling")
    
    messages = [{"role": "user", "content": user_message}]
    
    # Initial completion with tools
    response = litellm.completion(
        model=model,
        messages=messages,
        tools=AVAILABLE_TOOLS,
        tool_choice="auto"  # Let model decide when to use tools
    )
    
    response_message = response.choices[0].message
    
    # Check if model wants to call functions
    if response_message.tool_calls:
        # Add the assistant's response to messages
        messages.append({
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": response_message.tool_calls
        })
        
        # Execute each function call
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"Calling function: {function_name} with args: {function_args}")
            
            # Execute the function
            function_result = execute_function_call(function_name, function_args)
            
            # Add function result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(function_result)
            })
        
        # Get final response from model
        final_response = litellm.completion(
            model=model,
            messages=messages
        )
        
        return final_response.choices[0].message.content
    else:
        # No function calls needed
        return response_message.content

def demo_tool_calling():
    """
    Demonstrate tool calling with various examples.
    """
    print("=== LiteLLM Tool Calling Demo ===\n")
    
    test_cases = [
        "What is 25 + 37?",
        "Calculate 8 multiplied by 12",
        "What's the weather like in New York?",
        "Add 15.5 and 23.7, then tell me what you did",
        "Hello, how are you today?"  # No tool needed
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case}")
        try:
            result = chat_with_tools(test_case)
            print(f"Response: {result}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    demo_tool_calling()