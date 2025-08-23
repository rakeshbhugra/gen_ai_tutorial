"""
LiteLLM Tool Calling - Manual Dictionary Approach

This demonstrates defining tools manually using dictionaries.
More verbose but gives complete control over the tool schema.
Uses the modern 'tools' parameter (not deprecated 'functions').
"""

import json
import litellm
from dotenv import load_dotenv

load_dotenv()

def sum_numbers(a, b):
    """Add two numbers together."""
    return a + b

def multiply_numbers(a, b):
    """Multiply two numbers together."""
    return a * b

def get_current_weather(location, unit="fahrenheit"):
    """Get current weather for a location."""
    temp = 72 if unit == "fahrenheit" else 22
    return f"Weather in {location}: {temp}°{unit[0].upper()}, sunny"

# Manual function definitions - traditional approach
functions = [
    {
        "name": "sum_numbers",
        "description": "Add two numbers together and return the sum",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number to add"
                },
                "b": {
                    "type": "number", 
                    "description": "The second number to add"
                }
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "multiply_numbers",
        "description": "Multiply two numbers together and return the product",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number to multiply"
                },
                "b": {
                    "type": "number",
                    "description": "The second number to multiply"
                }
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "get_current_weather",
        "description": "Get the current weather for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use"
                }
            },
            "required": ["location"]
        }
    }
]

# Function mapping for execution
function_map = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
    "get_current_weather": get_current_weather
}

def demo_manual_functions():
    """Demonstrate manual function calling approach."""
    print("=== Manual Function Definition Approach ===\n")
    
    messages = [{"role": "user", "content": "What is 25 + 37?"}]
    
    # Convert functions to tools format
    tools = [{"type": "function", "function": func} for func in functions]
    
    # Call with manually defined tools
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

def test_multiple_cases():
    """Test multiple function calling scenarios."""
    print("\n=== Testing Multiple Cases ===\n")
    
    test_cases = [
        "What is 15 times 8?",
        "What's the weather in San Francisco?",
        "Add 100 and 200 together"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case}")
        
        messages = [{"role": "user", "content": test_case}]
        
        try:
            tools = [{"type": "function", "function": func} for func in functions]
            
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
    demo_manual_functions()
    test_multiple_cases()