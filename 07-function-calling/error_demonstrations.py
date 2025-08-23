"""
Error Demonstration Functions for LiteLLM

This module contains all the error demonstration functions that can be
imported and used in various error handling tutorials.
"""

import litellm
import openai
import time
from typing import Optional, Dict, Any

def demonstrate_authentication_error(original_key: Optional[str] = None):
    """
    Demonstrate AuthenticationError (401) - Invalid API credentials
    """
    print("=== AuthenticationError Demo ===")
    
    # Save original key if provided
    if not original_key:
        original_key = litellm.api_key
    
    results = {
        "error_type": "AuthenticationError",
        "status_code": 401,
        "caught": False,
        "message": None
    }
    
    try:
        # Use invalid API key
        litellm.api_key = "invalid_key_12345"
        
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
    except litellm.AuthenticationError as e:
        results["caught"] = True
        results["message"] = str(e.message)
        results["provider"] = e.llm_provider
        
        print(f"❌ Authentication failed: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print(f"   Provider: {e.llm_provider}")
        print("   💡 Solution: Check your API key configuration")
        
    except openai.AuthenticationError as e:
        # LiteLLM exceptions inherit from OpenAI exceptions
        results["caught"] = True
        print(f"❌ OpenAI-compatible auth error: {e}")
        
    finally:
        # Restore original key
        litellm.api_key = original_key
        print("✅ API key restored\n")
    
    return results

def demonstrate_bad_request_error():
    """
    Demonstrate BadRequestError (400) - Invalid request parameters
    """
    print("=== BadRequestError Demo ===")
    
    results = []
    
    # Test 1: Invalid model name
    try:
        response = litellm.completion(
            model="gpt-nonexistent-model",
            messages=[{"role": "user", "content": "Hello"}]
        )
    except litellm.BadRequestError as e:
        print(f"❌ Bad request: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print("   💡 Solution: Use valid model names like 'gpt-3.5-turbo'")
        results.append({
            "test": "invalid_model",
            "caught": True,
            "message": str(e.message)
        })
    
    # Test 2: Context window too large
    try:
        long_message = "x" * 100000  # Very long message
        response = litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": long_message}]
        )
    except litellm.BadRequestError as e:
        print(f"❌ Context window exceeded: {e.message}")
        print("   💡 Solution: Reduce message length or use a model with larger context window")
        results.append({
            "test": "context_window",
            "caught": True,
            "message": "Context window exceeded"
        })
    
    print("✅ BadRequestError handling complete\n")
    return results

def demonstrate_rate_limit_error():
    """
    Demonstrate RateLimitError (429) - API rate limits exceeded
    """
    print("=== RateLimitError Demo ===")
    
    results = {
        "requests_made": 0,
        "rate_limit_hit": False,
        "should_retry": False
    }
    
    try:
        # Make rapid successive calls to trigger rate limit
        for i in range(10):
            response = litellm.completion(
                model="gemini/gemini-2.5-flash-lite",
                messages=[{"role": "user", "content": f"Hello {i}"}],
                timeout=1
            )
            results["requests_made"] += 1
            print(f"Request {i+1} successful")
            
    except litellm.RateLimitError as e:
        results["rate_limit_hit"] = True
        results["should_retry"] = litellm._should_retry(e.status_code)
        
        print(f"❌ Rate limit exceeded: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print("   💡 Solution: Implement exponential backoff retry")
        print(f"   Should retry: {results['should_retry']}")
    
    print("✅ RateLimitError handling complete\n")
    return results

def demonstrate_timeout_error():
    """
    Demonstrate APITimeoutError - Request timeout
    """
    print("=== APITimeoutError Demo ===")
    
    results = {
        "timeout_caught": False,
        "error_type": None
    }
    
    try:
        # Set very short timeout to trigger error
        response = litellm.completion(
            model="gemini/gemini-2.5-flash-lite",
            messages=[{"role": "user", "content": "Write a long essay about AI"}],
            timeout=0.001  # 1ms timeout - will definitely fail
        )
        
    except openai.APITimeoutError as e:
        results["timeout_caught"] = True
        results["error_type"] = "APITimeoutError"
        print(f"❌ Request timeout: {e}")
        print("   💡 Solution: Increase timeout or implement retry with backoff")
        
    except litellm.APIConnectionError as e:
        results["timeout_caught"] = True
        results["error_type"] = "APIConnectionError"
        print(f"❌ Connection error (includes timeouts): {e.message}")
        print("   💡 Solution: Check network connection and increase timeout")
    
    print("✅ Timeout error handling complete\n")
    return results

def demonstrate_not_found_error():
    """
    Demonstrate NotFoundError (404) - Model or resource not found
    """
    print("=== NotFoundError Demo ===")
    
    results = {
        "error_caught": False,
        "actual_error_type": None
    }
    
    try:
        response = litellm.completion(
            model="gpt-8-super-advanced",  # Non-existent model
            messages=[{"role": "user", "content": "Hello"}]
        )
        
    except litellm.NotFoundError as e:
        results["error_caught"] = True
        results["actual_error_type"] = "NotFoundError"
        print(f"❌ Model not found: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print("   💡 Solution: Use supported model names")
        
    except litellm.BadRequestError as e:
        # Some providers return 400 instead of 404 for invalid models
        results["error_caught"] = True
        results["actual_error_type"] = "BadRequestError"
        print(f"❌ Invalid model (returned as BadRequest): {e.message}")
    
    print("✅ NotFoundError handling complete\n")
    return results

def demonstrate_unsupported_tool_error():
    """
    Demonstrate InternalServerError when using tools with unsupported models
    """
    print("=== Unsupported Tool Calling Demo ===")
    
    results = {
        "model": "gpt-3.5-turbo-instruct",
        "supports_tools": False,
        "error_type": None
    }
    
    tools = [{
        "type": "function",
        "function": {
            "name": "test_function",
            "description": "Test function",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }]
    
    model = results["model"]
    results["supports_tools"] = litellm.supports_function_calling(model)
    
    print(f"Model: {model}")
    print(f"Supports tools: {results['supports_tools']}")
    
    try:
        response = litellm.completion(
            model=model,
            prompt="Hello",  # Instruct models use 'prompt'
            tools=tools  # This will cause an error
        )
    except litellm.InternalServerError as e:
        results["error_type"] = "InternalServerError"
        print(f"❌ InternalServerError: Tools not supported")
        print(f"   Error: {str(e)[:100]}...")
        print("   💡 Solution: Check litellm.supports_function_calling() first")
    except Exception as e:
        results["error_type"] = type(e).__name__
        print(f"❌ {type(e).__name__}: {str(e)[:100]}...")
    
    print("✅ Unsupported tool error handling complete\n")
    return results

def demonstrate_error_information_extraction():
    """
    Show how to extract detailed error information
    """
    print("=== Error Information Extraction ===")
    
    error_details = {}
    
    try:
        response = litellm.completion(
            model="invalid-model-name",
            messages=[{"role": "user", "content": "Hello"}]
        )
        
    except litellm.BadRequestError as e:
        error_details = {
            "type": type(e).__name__,
            "message": e.message,
            "status_code": e.status_code,
            "provider": e.llm_provider,
            "has_response": hasattr(e, 'response'),
            "has_request": hasattr(e, 'request')
        }
        
        print("📊 Error Details:")
        print(f"   Type: {error_details['type']}")
        print(f"   Message: {error_details['message']}")
        print(f"   Status Code: {error_details['status_code']}")
        print(f"   Provider: {error_details['provider']}")
        
        if error_details['has_response']:
            print(f"   Has Response: Yes")
        if error_details['has_request']:
            print(f"   Has Request: Yes")
    
    print("✅ Error information extraction complete\n")
    return error_details

def demonstrate_function_calling_errors():
    """
    Demonstrate error handling specific to function/tool calling
    """
    print("=== Function Calling Error Handling ===")
    
    results = []
    
    # Test 1: Invalid tool definition
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
        results.append({
            "test": "invalid_tool_schema",
            "error": "BadRequestError",
            "caught": True
        })
    
    # Test 2: Function execution error handling
    def sample_function(x: int) -> int:
        if x < 0:
            raise ValueError("x must be non-negative")
        return x * 2
    
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
        results.append({
            "test": "function_execution",
            "error": "ValueError",
            "caught": True
        })
    
    print("✅ Function calling error handling complete\n")
    return results

def demonstrate_all_errors():
    """
    Run all error demonstrations and return summary
    """
    print("🚨 Running All Error Demonstrations 🚨\n")
    
    all_results = {
        "authentication": None,
        "bad_request": None,
        "rate_limit": None,
        "timeout": None,
        "not_found": None,
        "unsupported_tools": None,
        "error_extraction": None,
        "function_calling": None
    }
    
    # Run each demonstration
    all_results["authentication"] = demonstrate_authentication_error()
    all_results["bad_request"] = demonstrate_bad_request_error()
    # Commented out to avoid rate limits
    # all_results["rate_limit"] = demonstrate_rate_limit_error()
    # all_results["timeout"] = demonstrate_timeout_error()
    all_results["not_found"] = demonstrate_not_found_error()
    all_results["unsupported_tools"] = demonstrate_unsupported_tool_error()
    all_results["error_extraction"] = demonstrate_error_information_extraction()
    all_results["function_calling"] = demonstrate_function_calling_errors()
    
    return all_results