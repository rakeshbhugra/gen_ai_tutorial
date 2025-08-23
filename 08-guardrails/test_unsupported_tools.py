"""
Test what error we get when trying to use tools with models that don't support them.
"""

import litellm
from dotenv import load_dotenv
import json

load_dotenv()

# Enable verbose to see detailed errors
# litellm.set_verbose = True

def test_unsupported_model_tools():
    """Test tool calling with models that don't support it."""
    
    print("🧪 Testing Tool Calling with Unsupported Models\n")
    
    # Define a simple tool
    tools = [{
        "type": "function",
        "function": {
            "name": "sum_numbers",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        }
    }]
    
    # Test different models
    test_models = [
        "gpt-3.5-turbo-instruct",  # Doesn't support tools (uses Completions API)
        "babbage-002",  # Base model, doesn't support tools
        "davinci-002",  # Base model, doesn't support tools
        "gpt-3.5-turbo",  # DOES support tools (for comparison)
    ]
    
    for model in test_models:
        print(f"Testing model: {model}")
        print("-" * 40)
        
        # First check if model supports function calling
        try:
            supports_tools = litellm.supports_function_calling(model)
            print(f"  litellm.supports_function_calling(): {supports_tools}")
        except Exception as e:
            print(f"  Error checking support: {e}")
            supports_tools = None
        
        # Try to use tools with the model
        try:
            if model == "gpt-3.5-turbo-instruct":
                # This model uses completion endpoint, not chat
                response = litellm.completion(
                    model=model,
                    prompt="What is 2 + 2?",  # Use prompt for instruct model
                    tools=tools
                )
            else:
                # Chat models use messages
                response = litellm.completion(
                    model=model,
                    messages=[{"role": "user", "content": "What is 2 + 2?"}],
                    tools=tools
                )
            
            print(f"  ✅ Surprisingly worked! Response: {response.choices[0].message.content[:50]}...")
            
        except litellm.BadRequestError as e:
            print(f"  ❌ BadRequestError caught!")
            print(f"     Error message: {e.message}")
            print(f"     Status code: {e.status_code}")
            print(f"     Provider: {e.llm_provider}")
            
        except litellm.UnsupportedParamsError as e:
            print(f"  ❌ UnsupportedParamsError caught!")
            print(f"     Error message: {e.message}")
            print(f"     Status code: {e.status_code}")
            
        except litellm.NotFoundError as e:
            print(f"  ❌ NotFoundError - Model might not exist")
            print(f"     Error message: {e.message}")
            
        except Exception as e:
            print(f"  ❌ Other error: {type(e).__name__}")
            print(f"     Error: {str(e)}")
        
        print()
    
    # Also test with a definitely unsupported parameter combination
    print("Testing edge case: Completion model with chat-style parameters")
    print("-" * 40)
    try:
        response = litellm.completion(
            model="gpt-3.5-turbo-instruct",
            messages=[{"role": "user", "content": "Hello"}],  # Wrong! Should use 'prompt'
            tools=tools,
            temperature=0.7
        )
    except Exception as e:
        print(f"  ❌ {type(e).__name__}: {str(e)[:200]}...")

if __name__ == "__main__":
    test_unsupported_model_tools()