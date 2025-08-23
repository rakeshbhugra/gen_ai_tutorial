"""
LiteLLM Error Handling Tutorial (Refactored)

This module demonstrates comprehensive error handling for LiteLLM
by importing error demonstrations from a separate module for better
code organization and reusability.
"""

import time
import litellm
import openai
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List

# Import all error demonstrations
from error_demonstrations import (
    demonstrate_authentication_error,
    demonstrate_bad_request_error,
    demonstrate_rate_limit_error,
    demonstrate_timeout_error,
    demonstrate_not_found_error,
    demonstrate_unsupported_tool_error,
    demonstrate_error_information_extraction,
    demonstrate_function_calling_errors,
    demonstrate_all_errors
)

load_dotenv()

# ================================
# RETRY MECHANISMS
# ================================

def retry_with_exponential_backoff(
    func, 
    max_retries: int = 3, 
    base_delay: float = 1.0,
    max_delay: float = 60.0
):
    """
    Implement exponential backoff retry mechanism
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
    
    Returns:
        Result from successful function call
    
    Raises:
        Last exception if all retries fail
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
    
    Args:
        model: Model to use
        messages: Message list for the conversation
        **kwargs: Additional parameters for completion
    
    Returns:
        Completion response or None if error
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

# ================================
# ERROR HANDLING PATTERNS
# ================================

class ErrorHandler:
    """
    Centralized error handler for LiteLLM operations
    """
    
    def __init__(self, log_errors: bool = True):
        self.log_errors = log_errors
        self.error_counts = {}
        self.last_errors = {}
    
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle and categorize an error
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
        
        Returns:
            Dictionary with error details and recommendations
        """
        error_type = type(error).__name__
        
        # Update error statistics
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        self.last_errors[error_type] = {
            "message": str(error),
            "context": context,
            "timestamp": time.time()
        }
        
        # Categorize and provide recommendations
        if isinstance(error, litellm.AuthenticationError):
            return {
                "category": "authentication",
                "retryable": False,
                "action": "fix_credentials",
                "message": "Invalid API credentials. Check your API keys."
            }
        
        elif isinstance(error, litellm.BadRequestError):
            return {
                "category": "bad_request",
                "retryable": False,
                "action": "fix_request",
                "message": "Invalid request parameters. Review your input."
            }
        
        elif isinstance(error, litellm.RateLimitError):
            return {
                "category": "rate_limit",
                "retryable": True,
                "action": "retry_with_backoff",
                "message": "Rate limit exceeded. Implement backoff strategy."
            }
        
        elif isinstance(error, openai.APITimeoutError):
            return {
                "category": "timeout",
                "retryable": True,
                "action": "increase_timeout",
                "message": "Request timed out. Increase timeout or retry."
            }
        
        elif isinstance(error, litellm.NotFoundError):
            return {
                "category": "not_found",
                "retryable": False,
                "action": "check_resource",
                "message": "Resource not found. Verify model name or endpoint."
            }
        
        elif isinstance(error, litellm.InternalServerError):
            # Special check for unsupported tools
            if "tools" in str(error).lower():
                return {
                    "category": "unsupported_feature",
                    "retryable": False,
                    "action": "check_capabilities",
                    "message": "Model doesn't support this feature (likely tools/functions)."
                }
            return {
                "category": "server_error",
                "retryable": True,
                "action": "retry_later",
                "message": "Server error. May be temporary."
            }
        
        else:
            return {
                "category": "unknown",
                "retryable": False,
                "action": "investigate",
                "message": f"Unexpected error: {error_type}"
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get error statistics"""
        return {
            "error_counts": self.error_counts,
            "total_errors": sum(self.error_counts.values()),
            "last_errors": self.last_errors
        }

# ================================
# PRACTICAL EXAMPLES
# ================================

def safe_tool_calling_example():
    """
    Example of safe tool calling with proper error handling
    """
    print("=== Safe Tool Calling Example ===\n")
    
    model = "gpt-3.5-turbo-instruct"
    tools = [{
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    }]
    
    # Check capability first
    if litellm.supports_function_calling(model):
        print(f"✅ {model} supports tool calling")
        try:
            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": "Calculate 2+2"}],
                tools=tools
            )
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"❌ {model} doesn't support tool calling")
        print("   Using fallback prompt-based approach...")
        
        try:
            response = litellm.completion(
                model=model,
                prompt="Calculate 2+2. Answer: ",
                max_tokens=10
            )
            print(f"Fallback response: {response.choices[0].text}")
        except AttributeError:
            # Handle response format differences
            print("Note: Response format differs for completion models")

def circuit_breaker_example():
    """
    Example of circuit breaker pattern for fault tolerance
    """
    print("\n=== Circuit Breaker Example ===\n")
    
    class CircuitBreaker:
        def __init__(self, failure_threshold: int = 3, timeout: float = 60):
            self.failure_count = 0
            self.failure_threshold = failure_threshold
            self.timeout = timeout
            self.last_failure_time = None
            self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        
        def call(self, func):
            if self.state == "OPEN":
                if self.last_failure_time and (time.time() - self.last_failure_time < self.timeout):
                    raise Exception("Circuit breaker is OPEN - refusing requests")
                else:
                    self.state = "HALF_OPEN"
                    print("Circuit breaker entering HALF_OPEN state")
            
            try:
                result = func()
                if self.state == "HALF_OPEN":
                    print("Success in HALF_OPEN state - closing circuit")
                self.state = "CLOSED"
                self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    print(f"Circuit breaker OPEN after {self.failure_count} failures")
                
                raise e
    
    # Demo circuit breaker
    breaker = CircuitBreaker(failure_threshold=2)
    
    def potentially_failing_call():
        # Simulate a call that might fail
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise litellm.APIConnectionError("Simulated connection error")
        return "Success!"
    
    for i in range(5):
        try:
            result = breaker.call(potentially_failing_call)
            print(f"Attempt {i+1}: {result}")
        except Exception as e:
            print(f"Attempt {i+1}: Failed - {e}")
        
        time.sleep(0.5)

# ================================
# MAIN EXECUTION
# ================================

def main():
    """
    Run error handling demonstrations
    """
    print("🚨 LiteLLM Error Handling Tutorial 🚨\n")
    
    # Create error handler
    error_handler = ErrorHandler()
    
    # Menu for demonstrations
    print("Select demonstrations to run:")
    print("1. All error types")
    print("2. Retry mechanisms")
    print("3. Safe tool calling")
    print("4. Circuit breaker pattern")
    print("5. Individual error demos")
    
    # For tutorial, run key demos
    print("\n" + "="*50)
    print("Running selected demonstrations...")
    print("="*50 + "\n")
    
    # Individual error demos (imported from error_demonstrations)
    demonstrate_authentication_error()
    demonstrate_bad_request_error()
    demonstrate_unsupported_tool_error()
    
    # Advanced patterns
    safe_tool_calling_example()
    circuit_breaker_example()
    
    # Show error statistics
    print("\n" + "="*50)
    print("Error Handler Statistics:")
    print("="*50)
    
    # Simulate some errors for statistics
    test_errors = [
        litellm.AuthenticationError("Test auth error", llm_provider="openai", model="gpt-3.5-turbo"),
        litellm.BadRequestError("Test bad request", llm_provider="openai", model="gpt-3.5-turbo"),
        litellm.RateLimitError("Test rate limit", llm_provider="openai", model="gpt-3.5-turbo")
    ]
    
    for error in test_errors:
        result = error_handler.handle_error(error, context="test")
        print(f"{type(error).__name__}: {result['message']}")
    
    stats = error_handler.get_statistics()
    print(f"\nTotal errors handled: {stats['total_errors']}")
    print(f"Error breakdown: {stats['error_counts']}")
    
    print("\n🎉 Error handling tutorial complete!")
    print("\n💡 Key Takeaways:")
    print("1. Import error demonstrations for cleaner code")
    print("2. Use retry mechanisms for transient errors")
    print("3. Check capabilities before using features")
    print("4. Implement circuit breakers for resilience")
    print("5. Track error statistics for monitoring")

if __name__ == "__main__":
    main()