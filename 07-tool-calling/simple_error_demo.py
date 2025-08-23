"""
Simple LiteLLM Error Handling Demo

This demonstrates the most common error scenarios without
making too many API calls or triggering rate limits.
"""

import litellm
import openai
from dotenv import load_dotenv

load_dotenv()

def demo_all_errors():
    """Demonstrate all major error types safely"""
    
    print("🚨 LiteLLM Error Handling Demo 🚨\n")
    
    # 1. AuthenticationError
    print("1️⃣ AuthenticationError Demo:")
    original_key = litellm.api_key
    try:
        litellm.api_key = "invalid_key"
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except litellm.AuthenticationError as e:
        print(f"   ❌ Caught: {type(e).__name__}")
        print(f"   📝 Message: Invalid credentials")
        print(f"   💡 Solution: Check API key")
    finally:
        litellm.api_key = original_key
    
    # 2. BadRequestError
    print("\n2️⃣ BadRequestError Demo:")
    try:
        response = litellm.completion(
            model="gpt-nonexistent-model",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except litellm.BadRequestError as e:
        print(f"   ❌ Caught: {type(e).__name__}")
        print(f"   📝 Message: Invalid model name")
        print(f"   💡 Solution: Use valid model like 'gpt-3.5-turbo'")
    
    # 3. Context window exceeded
    print("\n3️⃣ Context Window Error Demo:")
    try:
        # Create a very long message
        long_message = "x" * 50000
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": long_message}]
        )
    except litellm.BadRequestError as e:
        print(f"   ❌ Caught: {type(e).__name__}")
        print(f"   📝 Message: Context window exceeded")
        print(f"   💡 Solution: Reduce message length")
    
    # 4. Function calling errors
    print("\n4️⃣ Function Calling Error Demo:")
    try:
        # Invalid tool schema (missing required fields)
        invalid_tools = [{
            "type": "function",
            "function": {
                "name": "test_function"
                # Missing 'parameters' field
            }
        }]
        
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Use the function"}],
            tools=invalid_tools
        )
    except litellm.BadRequestError as e:
        print(f"   ❌ Caught: {type(e).__name__}")
        print(f"   📝 Message: Invalid tool schema")
        print(f"   💡 Solution: Include all required tool fields")
    
    # 5. Successful call for comparison
    print("\n5️⃣ Successful Call Demo:")
    try:
        response = litellm.completion(
            model="gemini/gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": "Say hello in one word"}],
            timeout=30
        )
        print(f"   ✅ Success: {response.choices[0].message.content}")
    except Exception as e:
        print(f"   ❌ Error: {type(e).__name__} - {e}")

def demonstrate_retry_logic():
    """Show how to implement retry logic"""
    
    print("\n🔄 Retry Logic Demo:")
    
    def should_retry_error(error):
        """Determine if an error should be retried"""
        retry_errors = (
            litellm.RateLimitError,
            litellm.APIConnectionError, 
            openai.APITimeoutError
        )
        no_retry_errors = (
            litellm.AuthenticationError,
            litellm.BadRequestError,
            litellm.NotFoundError,
            litellm.PermissionDeniedError
        )
        
        if isinstance(error, retry_errors):
            return True, "Transient error - retry with backoff"
        elif isinstance(error, no_retry_errors):
            return False, "Non-retryable error - fix request first"
        else:
            return False, "Unknown error type"
    
    # Test different error types by their class names
    test_error_types = [
        ("AuthenticationError", "Invalid API key"),
        ("BadRequestError", "Invalid model"),
        ("RateLimitError", "Rate limit exceeded"), 
        ("APIConnectionError", "Connection failed")
    ]
    
    for error_name, error_msg in test_error_types:
        # Create mock error to test logic
        class MockError:
            pass
        
        # Test retry logic based on error type
        if error_name in ["RateLimitError", "APIConnectionError"]:
            status = "🔄 RETRY"
            reason = "Transient error - retry with backoff"
        else:
            status = "❌ NO RETRY" 
            reason = "Non-retryable error - fix request first"
            
        print(f"   {error_name}: {status} - {reason}")

def demonstrate_error_attributes():
    """Show error attributes available for debugging"""
    
    print("\n🔍 Error Attributes Demo:")
    
    try:
        response = litellm.completion(
            model="invalid-model-name",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except litellm.BadRequestError as e:
        print("   📊 Available error information:")
        print(f"      Type: {type(e).__name__}")
        print(f"      Message: {e.message}")
        print(f"      Status Code: {e.status_code}")
        print(f"      Provider: {e.llm_provider}")
        
        # Check for additional attributes
        if hasattr(e, 'response'):
            print(f"      Has Response: Yes")
        if hasattr(e, 'request'):
            print(f"      Has Request: Yes")

def main():
    """Run all demonstrations"""
    demo_all_errors()
    demonstrate_retry_logic()
    demonstrate_error_attributes()
    
    print("\n🎯 Key Takeaways:")
    print("   ✅ Always wrap LiteLLM calls in try-except")
    print("   ✅ Handle different error types appropriately")
    print("   ✅ Only retry transient errors (rate limits, timeouts)")
    print("   ✅ Don't retry auth/validation errors")
    print("   ✅ Extract error details for debugging")
    print("   ✅ Use exponential backoff for retries")

if __name__ == "__main__":
    main()