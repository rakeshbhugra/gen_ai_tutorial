"""
LiteLLM Tool Calling - function_to_dict Approach

This demonstrates using litellm.utils.function_to_dict() to automatically
generate tool schemas from Python functions and docstrings.
Much cleaner and less error-prone than manual definitions.
Uses the modern 'tools' parameter (not deprecated 'functions').
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
    
    Returns
    -------
    float
        The sum of the two numbers
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
    
    Returns
    -------
    float
        The product of the two numbers
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
    
    Returns
    -------
    str
        A description of the current weather
    """
    temp = 72 if unit == "fahrenheit" else 22
    return f"Weather in {location}: {temp}°{unit[0].upper()}, sunny"

# Use function_to_dict - automatically generates schema from docstrings!
tools = [
    {"type": "function", "function": litellm.utils.function_to_dict(sum_numbers)},
    {"type": "function", "function": litellm.utils.function_to_dict(multiply_numbers)},
    {"type": "function", "function": litellm.utils.function_to_dict(get_current_weather)}
]

for tool in tools:
    print(json.dumps(tool, indent=2))
    print("-"*40)

# Function mapping for execution
function_map = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
    "get_current_weather": get_current_weather
}

def demo_function_to_dict():
    """Demonstrate function_to_dict approach."""
    print("=== function_to_dict Approach ===\n")
    
    # Show what function_to_dict generates
    print("Generated function schema for sum_numbers:")
    print(json.dumps(litellm.utils.function_to_dict(sum_numbers), indent=2))
    print()
    
    messages = [{"role": "user", "content": "What is 25 + 37?"}]
    
    # Call with auto-generated tools
    response = litellm.completion(
        model="gemini/gemini-2.5-flash-lite",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    print(f"Model response: {response_message}")
    
    # Check if model wants to call a function
    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"\nFunction called: {function_name}")
        print(f"Arguments: {function_args}")
        
        # Execute the function
        if function_name in function_map:
            result = function_map[function_name](**function_args)
            print(f"Function result: {result}")
            
            # Send function result back to model
            messages.append({
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": response_message.tool_calls
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
            
            # Get final response
            final_response = litellm.completion(
                model="gemini/gemini-2.5-flash-lite",
                messages=messages
            )
            
            print(f"\nFinal response: {final_response.choices[0].message.content}")

def compare_schemas():
    """Compare auto-generated vs manual schemas."""
    print("\n=== Schema Comparison ===\n")
    
    # Show auto-generated schema
    auto_schema = litellm.utils.function_to_dict(sum_numbers)
    print("Auto-generated schema:")
    print(json.dumps(auto_schema, indent=2))
    
    # Manual equivalent
    manual_schema = {
        "name": "sum_numbers",
        "description": "Add two numbers together and return the sum",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number to add"},
                "b": {"type": "number", "description": "The second number to add"}
            },
            "required": ["a", "b"]
        }
    }
    
    print("\nManual equivalent:")
    print(json.dumps(manual_schema, indent=2))

def test_multiple_cases():
    """Test multiple function calling scenarios."""
    print("\n=== Testing Multiple Cases ===\n")
    
    test_cases = [
        "What is 15 times 8?",
        "What's the weather in San Francisco in celsius?",
        "Add 100 and 200 together"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case}")
        
        messages = [{"role": "user", "content": test_case}]
        
        try:
            response = litellm.completion(
                model="gemini/gemini-2.5-flash-lite",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            
            if response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"  Function: {function_name}({function_args})")
                
                if function_name in function_map:
                    result = function_map[function_name](**function_args)
                    print(f"  Result: {result}")
            else:
                print(f"  Direct response: {response_message.content}")
                
        except Exception as e:
            print(f"  Error: {e}")
        
        print()

if __name__ == "__main__":
    demo_function_to_dict()
    compare_schemas()
    test_multiple_cases()