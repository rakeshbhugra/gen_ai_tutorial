from manual_tool_calling import (
    sum_numbers,
    multiply_numbers,
    get_current_weather
)
import litellm

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

print("Response:", response["choices"][0]["message"]["content"])