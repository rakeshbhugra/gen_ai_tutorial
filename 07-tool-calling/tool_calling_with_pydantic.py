"""
LiteLLM Tool Calling - Pydantic Approach

This demonstrates using Pydantic models to define tool schemas with automatic
validation and type safety. The cleanest and most maintainable approach.
Uses the modern 'tools' parameter (not deprecated 'functions').
"""

import json
import litellm
from typing import Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Pydantic models for tool parameters
class SumNumbersInput(BaseModel):
    """Input schema for sum_numbers function."""
    a: float = Field(..., description="The first number to add")
    b: float = Field(..., description="The second number to add")

class MultiplyNumbersInput(BaseModel):
    """Input schema for multiply_numbers function."""
    a: float = Field(..., description="The first number to multiply")
    b: float = Field(..., description="The second number to multiply")

class WeatherInput(BaseModel):
    """Input schema for get_current_weather function."""
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")
    unit: Literal["celsius", "fahrenheit"] = Field(
        default="fahrenheit", 
        description="The temperature unit to use"
    )

# Function implementations
def sum_numbers(a: float, b: float) -> float:
    """Add two numbers together and return the sum."""
    return a + b

def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together and return the product."""
    return a * b

def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather for a specific location."""
    temp = 72 if unit == "fahrenheit" else 22
    return f"Weather in {location}: {temp}°{unit[0].upper()}, sunny"

# Convert Pydantic models to OpenAI tool format
def pydantic_to_tool(model_class: BaseModel, func_name: str, description: str) -> dict:
    """Convert a Pydantic model to OpenAI tool format."""
    schema = model_class.model_json_schema()
    
    return {
        "type": "function",
        "function": {
            "name": func_name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": schema["properties"],
                "required": schema.get("required", [])
            }
        }
    }

# Generate tools from Pydantic models
tools = [
    pydantic_to_tool(
        SumNumbersInput, 
        "sum_numbers", 
        "Add two numbers together and return the sum"
    ),
    pydantic_to_tool(
        MultiplyNumbersInput, 
        "multiply_numbers", 
        "Multiply two numbers together and return the product"
    ),
    pydantic_to_tool(
        WeatherInput, 
        "get_current_weather", 
        "Get the current weather for a specific location"
    )
]

# Function mapping for execution with Pydantic validation
function_map = {
    "sum_numbers": (sum_numbers, SumNumbersInput),
    "multiply_numbers": (multiply_numbers, MultiplyNumbersInput),
    "get_current_weather": (get_current_weather, WeatherInput)
}

def execute_function_with_validation(function_name: str, arguments: dict):
    """Execute function with Pydantic validation."""
    if function_name not in function_map:
        raise ValueError(f"Unknown function: {function_name}")
    
    func, input_model = function_map[function_name]
    
    # Validate input using Pydantic model
    try:
        validated_input = input_model(**arguments)
        # Execute function with validated parameters
        result = func(**validated_input.model_dump())
        return result
    except Exception as e:
        raise ValueError(f"Validation error for {function_name}: {e}")

def demo_pydantic_tools():
    """Demonstrate Pydantic-based tool calling."""
    print("=== Pydantic Tool Definition Approach ===\n")
    
    # Show generated tool schema
    print("Generated tool schema for sum_numbers:")
    print(json.dumps(tools[0], indent=2))
    print()
    
    messages = [{"role": "user", "content": "What is 25 + 37?"}]
    
    # Call with Pydantic-generated tools
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
        
        # Execute with validation
        try:
            result = execute_function_with_validation(function_name, function_args)
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
            
        except ValueError as e:
            print(f"Validation error: {e}")

def test_validation():
    """Test Pydantic validation with invalid inputs."""
    print("\n=== Testing Pydantic Validation ===\n")
    
    # Test valid input
    print("1. Valid input:")
    try:
        result = execute_function_with_validation("sum_numbers", {"a": 10, "b": 20})
        print(f"   Result: {result}")
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Test invalid input - missing required field
    print("\n2. Invalid input (missing required field):")
    try:
        result = execute_function_with_validation("sum_numbers", {"a": 10})
        print(f"   Result: {result}")
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Test invalid input - wrong type
    print("\n3. Invalid input (wrong type):")
    try:
        result = execute_function_with_validation("sum_numbers", {"a": "not_a_number", "b": 20})
        print(f"   Result: {result}")
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Test enum validation
    print("\n4. Invalid enum value:")
    try:
        result = execute_function_with_validation("get_current_weather", {
            "location": "San Francisco, CA", 
            "unit": "kelvin"  # Invalid unit
        })
        print(f"   Result: {result}")
    except ValueError as e:
        print(f"   Error: {e}")

def compare_approaches():
    """Compare different tool definition approaches."""
    print("\n=== Approach Comparison ===\n")
    
    print("1. Manual Dictionary (most verbose):")
    print("   + Complete control over schema")
    print("   - Very verbose and error-prone")
    print("   - No automatic validation")
    print("   - Hard to maintain")
    
    print("\n2. function_to_dict (moderate):")
    print("   + Auto-generates from docstrings")
    print("   + Less verbose than manual")
    print("   - Limited validation")
    print("   - Docstring format dependent")
    
    print("\n3. Pydantic (cleanest):")
    print("   + Type safety and validation")
    print("   + Clean, declarative syntax")
    print("   + Auto-generates JSON schema")
    print("   + IDE support and intellisense")
    print("   + Automatic data validation")
    print("   - Requires Pydantic dependency")

def test_multiple_cases():
    """Test multiple function calling scenarios with validation."""
    print("\n=== Testing Multiple Cases with Validation ===\n")
    
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
                
                # Execute with validation
                try:
                    result = execute_function_with_validation(function_name, function_args)
                    print(f"  Result: {result}")
                except ValueError as ve:
                    print(f"  Validation Error: {ve}")
            else:
                print(f"  Direct response: {response_message.content}")
                
        except Exception as e:
            print(f"  Error: {e}")
        
        print()

if __name__ == "__main__":
    demo_pydantic_tools()
    test_validation()
    compare_approaches()
    test_multiple_cases()