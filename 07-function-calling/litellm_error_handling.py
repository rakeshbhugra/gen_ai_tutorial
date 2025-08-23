"""
LiteLLM Error Handling Tutorial

This module demonstrates comprehensive error handling for LiteLLM,
including all exception types, retry mechanisms, and best practices.

LiteLLM maps all provider errors to OpenAI-compatible exceptions for
consistent error handling across different LLM providers.
"""

import time
import json
import litellm
import openai
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()

# Enable debug mode to see detailed error information
# litellm.set_verbose = True

def demonstrate_authentication_error():
    """
    AuthenticationError (401) - Invalid API credentials
    """
    print("=== AuthenticationError Demo ===")
    
    # Save original key
    original_key = litellm.api_key
    
    try:
        # Use invalid API key
        litellm.api_key = "invalid_key_12345"
        
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
    except litellm.AuthenticationError as e:
        print(f"❌ Authentication failed: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print(f"   Provider: {e.llm_provider}")
        print("   💡 Solution: Check your API key configuration")
        
    except openai.AuthenticationError as e:
        # LiteLLM exceptions inherit from OpenAI exceptions
        print(f"❌ OpenAI-compatible auth error: {e}")
        
    finally:
        # Restore original key
        litellm.api_key = original_key
        print("✅ API key restored\n")

def demonstrate_bad_request_error():
    """
    BadRequestError (400) - Invalid request parameters
    """
    print("=== BadRequestError Demo ===")
    
    try:
        # Invalid model name
        response = litellm.completion(
            model="gpt-nonexistent-model",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
    except litellm.BadRequestError as e:
        print(f"❌ Bad request: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print("   💡 Solution: Use valid model names like 'gpt-3.5-turbo'")
        
    try:
        # Context window too large
        long_message = "x" * 100000  # Very long message
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": long_message}]
        )
        
    except litellm.BadRequestError as e:
        print(f"❌ Context window exceeded: {e.message}")
        print("   💡 Solution: Reduce message length or use a model with larger context window")
        
    print("✅ BadRequestError handling complete\n")

def demonstrate_rate_limit_error():
    """
    RateLimitError (429) - API rate limits exceeded
    """
    print("=== RateLimitError Demo ===")
    
    try:
        # Make rapid successive calls to trigger rate limit
        for i in range(10):
            response = litellm.completion(
                model="gemini/gemini-2.5-flash-lite",
                messages=[{"role": "user", "content": f"Hello {i}"}],
                timeout=1
            )
            print(f"Request {i+1} successful")
            
    except litellm.RateLimitError as e:
        print(f"❌ Rate limit exceeded: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print("   💡 Solution: Implement exponential backoff retry")
        
        # Check if we should retry
        should_retry = litellm._should_retry(e.status_code)
        print(f"   Should retry: {should_retry}")
        
    print("✅ RateLimitError handling complete\n")

def demonstrate_timeout_error():
    """
    APITimeoutError - Request timeout
    """
    print("=== APITimeoutError Demo ===")
    
    try:
        # Set very short timeout to trigger error
        response = litellm.completion(
            model="gemini/gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": "Write a long essay about AI"}],
            timeout=0.001  # 1ms timeout - will definitely fail
        )
        
    except openai.APITimeoutError as e:
        print(f"❌ Request timeout: {e}")
        print("   💡 Solution: Increase timeout or implement retry with backoff")
        
    except litellm.APIConnectionError as e:
        print(f"❌ Connection error (includes timeouts): {e.message}")
        print("   💡 Solution: Check network connection and increase timeout")
        
    print("✅ Timeout error handling complete\n")

def demonstrate_not_found_error():
    """
    NotFoundError (404) - Model or resource not found
    """
    print("=== NotFoundError Demo ===")
    
    try:
        response = litellm.completion(
            model="gpt-8-super-advanced",  # Non-existent model
            messages=[{"role": "user", "content": "Hello"}]
        )
        
    except litellm.NotFoundError as e:
        print(f"❌ Model not found: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print("   💡 Solution: Use supported model names")
        
    except litellm.BadRequestError as e:
        # Some providers return 400 instead of 404 for invalid models
        print(f"❌ Invalid model (returned as BadRequest): {e.message}")
        
    print("✅ NotFoundError handling complete\n")

def retry_with_exponential_backoff(
    func, 
    max_retries: int = 3, 
    base_delay: float = 1.0,
    max_delay: float = 60.0
):
    """
    Implement exponential backoff retry mechanism
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
            
        except (litellm.RateLimitError, litellm.APIConnectionError, openai.APITimeoutError) as e:
            if attempt == max_retries:
                print(f"❌ Max retries ({max_retries}) exceeded")
                raise e
                
            # Calculate delay with exponential backoff
            delay = min(base_delay * (2 ** attempt), max_delay)
            print(f"⏳ Retry {attempt + 1}/{max_retries} after {delay:.1f}s due to: {type(e).__name__}")
            time.sleep(delay)
            
        except (litellm.AuthenticationError, litellm.BadRequestError, litellm.NotFoundError) as e:
            # Don't retry on these errors - they won't succeed
            print(f"❌ Non-retryable error: {type(e).__name__} - {e.message}")
            raise e

def robust_completion(model: str, messages: list, **kwargs) -> Optional[Dict[Any, Any]]:
    """
    Robust completion function with comprehensive error handling
    """
    def make_request():
        return litellm.completion(
            model=model,
            messages=messages,
            **kwargs
        )
    
    try:
        return retry_with_exponential_backoff(make_request)
        
    except litellm.AuthenticationError as e:
        print(f"🔑 Authentication Error: Check your API keys")
        print(f"   Provider: {e.llm_provider}")
        return None
        
    except litellm.BadRequestError as e:
        print(f"📝 Bad Request: {e.message}")
        print(f"   Suggestion: Validate your request parameters")
        return None
        
    except litellm.RateLimitError as e:
        print(f"🚦 Rate Limited: {e.message}")
        print(f"   Suggestion: Implement request queuing or use different model")
        return None
        
    except litellm.NotFoundError as e:
        print(f"🔍 Not Found: {e.message}")
        print(f"   Suggestion: Check model availability")
        return None
        
    except Exception as e:
        print(f"🚨 Unexpected error: {type(e).__name__} - {e}")
        return None

def demonstrate_error_information_extraction():
    """
    Show how to extract detailed error information
    """
    print("=== Error Information Extraction ===")
    
    try:
        response = litellm.completion(
            model="invalid-model-name",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
    except litellm.BadRequestError as e:
        print("📊 Error Details:")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print(f"   Provider: {e.llm_provider}")
        
        # Check if error has additional attributes
        if hasattr(e, 'response'):
            print(f"   Response: {e.response}")
        if hasattr(e, 'request'):
            print(f"   Request: {e.request}")
            
    print("✅ Error information extraction complete\n")

def demonstrate_function_calling_errors():
    """
    Demonstrate error handling specific to function calling
    """
    print("=== Function Calling Error Handling ===")
    
    def sample_function(x: int) -> int:
        if x < 0:
            raise ValueError("x must be non-negative")
        return x * 2
    
    # Invalid tool definition
    try:
        invalid_tools = [
            {
                "type": "function",
                "function": {
                    "name": "sample_function",
                    # Missing required 'parameters' field
                    "description": "Sample function"
                }
            }
        ]
        
        response = litellm.completion(
            model="gemini/gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": "Use the function"}],
            tools=invalid_tools
        )
        
    except litellm.BadRequestError as e:
        print(f"❌ Invalid tool definition: {e.message}")
        print("   💡 Solution: Ensure all required tool schema fields are present")
        
    # Function execution error handling
    try:
        # This would be in the tool execution part
        result = sample_function(-5)  # This will raise ValueError
        
    except ValueError as e:
        print(f"❌ Function execution error: {e}")
        print("   💡 Solution: Validate function inputs before execution")
        
        # Return error to model
        error_message = {
            "role": "tool",
            "content": f"Error: {str(e)}",
            "tool_call_id": "some_id"
        }
        print(f"   Return to model: {error_message}")
        
    print("✅ Function calling error handling complete\n")

def main():
    """
    Run all error handling demonstrations
    """
    print("🚨 LiteLLM Error Handling Tutorial 🚨\n")
    
    # Run all demonstrations
    demonstrate_authentication_error()
    demonstrate_bad_request_error()
    demonstrate_rate_limit_error()
    demonstrate_timeout_error()
    demonstrate_not_found_error()
    demonstrate_error_information_extraction()
    demonstrate_function_calling_errors()
    
    # Test robust completion function
    print("=== Robust Completion Test ===")
    result = robust_completion(
        model="gemini/gemini-2.5-flash-lite",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        timeout=30
    )
    
    if result:
        print("✅ Robust completion successful!")
        print(f"   Response: {result.choices[0].message.content}")
    else:
        print("❌ Robust completion failed")
        
    print("\n🎉 Error handling tutorial complete!")
    print("\n💡 Key Takeaways:")
    print("   1. Always wrap LiteLLM calls in try-except blocks")
    print("   2. Handle different error types appropriately")
    print("   3. Implement retry logic for transient errors")
    print("   4. Don't retry authentication or bad request errors")
    print("   5. Extract error details for better debugging")
    print("   6. Use litellm._should_retry() for retry decisions")

if __name__ == "__main__":
    main()