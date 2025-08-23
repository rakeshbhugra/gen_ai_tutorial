"""
Clean test to identify the exact error when using tools with unsupported models.
"""

import litellm
from dotenv import load_dotenv

load_dotenv()

def test_tools_with_models():
    """Test what happens with different models and tools."""
    
    print("🔍 Testing Tool Support and Errors\n")
    
    # Simple tool definition
    tools = [{
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }]
    
    # Test 1: Model that supports tools
    print("1. Model WITH tool support (gpt-3.5-turbo):")
    print(f"   Supports tools: {litellm.supports_function_calling('gpt-3.5-turbo')}")
    try:
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "What is 5 + 3?"}],
            tools=tools,
            max_tokens=50
        )
        if response.choices[0].message.tool_calls:
            print(f"   ✅ Tool called: {response.choices[0].message.tool_calls[0].function.name}")
        else:
            print(f"   ✅ Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"   ❌ {type(e).__name__}: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Model that doesn't support tools (instruct model)
    print("2. Model WITHOUT tool support (gpt-3.5-turbo-instruct):")
    print(f"   Supports tools: {litellm.supports_function_calling('gpt-3.5-turbo-instruct')}")
    
    # First try with proper format for instruct model (no tools)
    print("\n   a) Correct usage (no tools):")
    try:
        response = litellm.completion(
            model="gpt-3.5-turbo-instruct",
            prompt="What is 5 + 3? Answer with just the number.",
            max_tokens=10
        )
        print(f"      ✅ Response: {response.choices[0].text.strip()}")
    except Exception as e:
        print(f"      ❌ {type(e).__name__}: {e}")
    
    # Now try with tools (should fail)
    print("\n   b) Incorrect usage (with tools):")
    try:
        response = litellm.completion(
            model="gpt-3.5-turbo-instruct",
            prompt="What is 5 + 3?",
            tools=tools  # This should cause an error
        )
        print(f"      ✅ Unexpectedly worked!")
    except litellm.InternalServerError as e:
        print(f"      ❌ InternalServerError (500)")
        print(f"         Message: {str(e)[:100]}...")
    except litellm.BadRequestError as e:
        print(f"      ❌ BadRequestError (400)")
        print(f"         Message: {e.message}")
    except litellm.UnsupportedParamsError as e:
        print(f"      ❌ UnsupportedParamsError")
        print(f"         Message: {e.message}")
    except Exception as e:
        print(f"      ❌ {type(e).__name__}")
        print(f"         Message: {str(e)[:100]}...")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Check if litellm can catch this earlier
    print("3. Pre-checking with litellm.supports_function_calling():")
    
    models_to_check = [
        "gpt-4",
        "gpt-3.5-turbo", 
        "gpt-3.5-turbo-instruct",
        "text-davinci-003",  # Deprecated but for reference
        "babbage-002"
    ]
    
    for model in models_to_check:
        try:
            supports = litellm.supports_function_calling(model)
            print(f"   {model}: {'✅ Supports tools' if supports else '❌ No tool support'}")
        except Exception as e:
            print(f"   {model}: ⚠️ Error checking: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Best practice demonstration
    print("4. BEST PRACTICE - Check before using:")
    model = "gpt-3.5-turbo-instruct"
    
    if litellm.supports_function_calling(model):
        print(f"   Model {model} supports tools, using them...")
        # Use tools
    else:
        print(f"   Model {model} doesn't support tools, using prompt engineering instead...")
        try:
            # Fallback to prompt-based approach
            prompt = """You have access to these functions:
- add(a, b): Add two numbers

User: What is 5 + 3?

If you need to use a function, respond with: FUNCTION: function_name(args)
Otherwise, respond normally.

Answer:"""
            
            response = litellm.completion(
                model=model,
                prompt=prompt,
                max_tokens=50
            )
            print(f"   Response: {response.choices[0].text.strip()}")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    test_tools_with_models()