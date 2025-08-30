# LiteLLM Error Handling Complete Guide (2025 Edition)

## Overview

LiteLLM maps all provider-specific errors to OpenAI-compatible exceptions, ensuring consistent error handling across different LLM providers (OpenAI, Anthropic, Google, etc.). This guide covers the current implementation as of 2025.

## Exception Hierarchy

All LiteLLM exceptions inherit from OpenAI exceptions:

```
BaseException
└── OpenAI Exceptions
    ├── AuthenticationError (401)
    ├── BadRequestError (400)
    ├── PermissionDeniedError (403)
    ├── NotFoundError (404)
    ├── RateLimitError (429)
    ├── APITimeoutError (408)
    ├── APIConnectionError (500+)
    └── InternalServerError (500)
```

## Modern Import Patterns

**✅ Correct imports for OpenAI SDK v1.0+ and LiteLLM:**

```python
# LiteLLM exceptions
import litellm
from litellm import completion

# OpenAI exceptions (for timeout errors)
import openai
from openai import AuthenticationError, BadRequestError, RateLimitError

# Alternative approach
try:
    response = litellm.completion(...)
except openai.BadRequestError as e:  # Use openai. prefix
    # Handle error
except litellm.AuthenticationError as e:  # Or litellm. prefix
    # Handle error
```

**❌ Outdated imports (don't use):**
```python
# This no longer works in OpenAI SDK v1.0+
from openai.error import OpenAIError, RateLimitError
```

## Error Types and Handling

### 1. AuthenticationError (401)

**When it occurs:**
- Invalid API key
- Expired credentials
- Missing authentication

**Example:**
```python
import litellm
import openai

try:
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except (litellm.AuthenticationError, openai.AuthenticationError) as e:
    print(f"Auth failed: {e}")
    print(f"Provider: {getattr(e, 'llm_provider', 'unknown')}")
    # Don't retry - fix credentials first
```

**Should you retry?** ❌ No - Fix credentials first

### 2. BadRequestError (400)

**When it occurs:**
- Invalid model name
- Context window exceeded
- Malformed request parameters
- Invalid tool definitions

**Example:**
```python
try:
    response = litellm.completion(
        model="gpt-nonexistent",  # Invalid model
        messages=[{"role": "user", "content": "Hello"}]
    )
except (litellm.BadRequestError, openai.BadRequestError) as e:
    print(f"Bad request: {e}")
    if "model" in str(e).lower():
        print("Use a valid model name")
    elif "context" in str(e).lower():
        print("Reduce message length")
    elif "tool" in str(e).lower():
        print("Fix tool definition")
```

**Should you retry?** ❌ No - Fix the request first

### 3. PermissionDeniedError (403)

**When it occurs:**
- Insufficient permissions for model/feature
- Account limitations
- Region restrictions

**Example:**
```python
try:
    response = litellm.completion(
        model="gpt-4",  # May require higher tier
        messages=[{"role": "user", "content": "Hello"}]
    )
except (litellm.PermissionDeniedError, openai.PermissionDeniedError) as e:
    print(f"Permission denied: {e}")
    print("Check your account tier and model access")
```

**Should you retry?** ❌ No - Check account permissions

### 4. NotFoundError (404)

**When it occurs:**
- Model doesn't exist
- Endpoint not found
- Resource not available

**Example:**
```python
try:
    response = litellm.completion(
        model="gpt-8",  # Doesn't exist
        messages=[{"role": "user", "content": "Hello"}]
    )
except (litellm.NotFoundError, openai.NotFoundError) as e:
    print(f"Not found: {e}")
    print("Check model availability")
```

**Should you retry?** ❌ No - Use valid model names

### 5. RateLimitError (429)

**When it occurs:**
- Too many requests per minute/day
- Token quota exceeded
- Concurrent request limits

**Example:**
```python
import time

try:
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except (litellm.RateLimitError, openai.RateLimitError) as e:
    print(f"Rate limited: {e}")
    
    # Safe retry check with error handling
    try:
        if hasattr(e, 'status_code') and isinstance(e.status_code, int):
            should_retry = litellm._should_retry(e.status_code)
            if should_retry:
                time.sleep(60)  # Wait before retry
        else:
            # Status code might be empty string - assume retryable
            time.sleep(60)
    except (TypeError, AttributeError):
        # Fallback for known _should_retry bugs
        time.sleep(60)
```

**Should you retry?** ✅ Yes - With exponential backoff

### 6. APITimeoutError (408)

**When it occurs:**
- Request takes too long
- Network timeout
- Server processing timeout

**Example:**
```python
try:
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}],
        timeout=0.1  # Very short timeout
    )
except openai.APITimeoutError as e:
    print(f"Timeout: {e}")
    # Increase timeout or retry
```

**Should you retry?** ✅ Yes - With longer timeout

### 7. APIConnectionError (500+) & InternalServerError

**When it occurs:**
- Network connectivity issues
- Server errors (500, 502, 503)
- Provider downtime

**Example:**
```python
try:
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except (litellm.APIConnectionError, litellm.InternalServerError) as e:
    print(f"Connection/Server error: {e}")
    print(f"Status: {getattr(e, 'status_code', 'unknown')}")
```

**Should you retry?** ✅ Yes - Server errors are often temporary

## Retry Strategy Decision Tree

```
Error occurred
├── AuthenticationError? → ❌ Don't retry, fix credentials
├── BadRequestError? → ❌ Don't retry, fix request
├── PermissionDeniedError? → ❌ Don't retry, check permissions
├── NotFoundError? → ❌ Don't retry, use valid resource
├── RateLimitError? → ✅ Retry with backoff
├── APITimeoutError? → ✅ Retry with longer timeout
├── APIConnectionError? → ✅ Retry with backoff
└── InternalServerError? → ✅ Retry with backoff
```

## Robust Exponential Backoff Implementation

```python
import time
import random
import litellm
import openai

def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    """Retry function with exponential backoff and proper error handling."""
    
    retryable_exceptions = (
        litellm.RateLimitError, 
        litellm.APIConnectionError,
        litellm.InternalServerError,
        openai.RateLimitError,
        openai.APITimeoutError,
        openai.APIConnectionError
    )
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except retryable_exceptions as e:
            if attempt == max_retries:
                raise e
            
            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Retrying in {delay:.1f}s... (attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)
        except Exception as e:
            # Non-retryable error - fail immediately
            print(f"Non-retryable error: {type(e).__name__}: {e}")
            raise
```

## Error Information Extraction

Every LiteLLM exception provides additional attributes:

```python
try:
    response = litellm.completion(...)
except Exception as e:
    # Standard exception info
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
    
    # LiteLLM-specific attributes (if available)
    if hasattr(e, 'status_code'):
        print(f"Status Code: {e.status_code}")
    if hasattr(e, 'llm_provider'):
        print(f"Provider: {e.llm_provider}")
    if hasattr(e, 'message'):
        print(f"Detailed Message: {e.message}")
```

## Function Calling Error Handling

### Checking Model Support

```python
import litellm

def safe_completion_with_tools(model, messages, tools=None):
    """Safely call completion with tools, checking support first."""
    
    # Check if model supports function calling
    if tools and not litellm.supports_function_calling(model):
        print(f"Model {model} doesn't support function calling")
        # Option 1: Use without tools
        return litellm.completion(model=model, messages=messages)
        
        # Option 2: Fallback to a model that supports tools
        # return litellm.completion(model="gpt-3.5-turbo", messages=messages, tools=tools)
    
    return litellm.completion(model=model, messages=messages, tools=tools)
```

### Completions API vs Chat Completions API

**Important distinction for instruction-tuned models:**

```python
# Models that use Completions API (NOT Chat Completions)
completions_models = [
    "gpt-3.5-turbo-instruct",
    "davinci-002",
    "babbage-002"
]

def completion_with_model_check(model, messages):
    """Handle different API types appropriately."""
    
    if model in completions_models:
        # These models don't support tools and use different parameters
        # Convert messages to prompt
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        return litellm.completion(
            model=model,
            prompt=prompt  # Use 'prompt' not 'messages'
            # Note: 'tools' parameter not supported
        )
    else:
        # Standard chat completion models
        return litellm.completion(
            model=model,
            messages=messages
            # tools can be used here if needed
        )
```

### Tool Definition Errors

```python
def validate_tool_schema(tools):
    """Basic validation for tool schemas."""
    for tool in tools:
        if tool.get("type") != "function":
            raise ValueError("Only 'function' type tools are supported")
        
        function = tool.get("function", {})
        if not function.get("name"):
            raise ValueError("Function name is required")
        if not function.get("parameters"):
            raise ValueError("Function parameters are required")

try:
    tools = [{"type": "function", "function": {"name": "test"}}]  # Missing parameters
    validate_tool_schema(tools)  # This will catch the error early
    
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Use tool"}],
        tools=tools
    )
except ValueError as e:
    print(f"Tool validation error: {e}")
except (litellm.BadRequestError, openai.BadRequestError) as e:
    print(f"API rejected tool definition: {e}")
```

### Function Execution Errors

```python
def safe_function_executor(function_name, function_args, available_functions):
    """Safely execute functions with error handling."""
    try:
        if function_name not in available_functions:
            return f"Error: Function '{function_name}' not found"
        
        result = available_functions[function_name](**function_args)
        return result
    except Exception as e:
        return f"Error executing {function_name}: {str(e)}"

# Example usage in function calling flow
def handle_tool_calls(tool_calls, messages, available_functions):
    """Process tool calls and add results to messages."""
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # Safe execution
        result = safe_function_executor(function_name, function_args, available_functions)
        
        # Add result to messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })
    
    return messages
```

## Best Practices

### 1. Graceful Degradation with Model Fallbacks

```python
def robust_completion(model, messages, fallback_models=None):
    """Attempt completion with fallbacks for reliability."""
    if fallback_models is None:
        fallback_models = ["gpt-3.5-turbo", "gpt-4o-mini"]
    
    models_to_try = [model] + fallback_models
    
    for current_model in models_to_try:
        try:
            return litellm.completion(model=current_model, messages=messages)
        except (litellm.NotFoundError, litellm.PermissionDeniedError, 
                openai.NotFoundError, openai.PermissionDeniedError) as e:
            print(f"Model {current_model} unavailable: {e}")
            if current_model == models_to_try[-1]:
                raise  # Re-raise if all models failed
            continue
        except Exception as e:
            # For other errors, don't try fallbacks
            raise
    
    raise Exception("All models failed")
```

### 2. Circuit Breaker Pattern

```python
import time
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout_seconds=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout_seconds
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if (datetime.now() - self.last_failure_time).seconds >= self.timeout:
                self.state = "HALF_OPEN"
                print("Circuit breaker moving to HALF_OPEN")
            else:
                raise Exception(f"Circuit breaker is OPEN. Try again after {self.timeout}s")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure(e)
            raise
    
    def on_success(self):
        if self.state == "HALF_OPEN":
            print("Circuit breaker: Service recovered, moving to CLOSED")
        self.failure_count = 0
        self.state = "CLOSED"
    
    def on_failure(self, exception):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            print(f"Circuit breaker OPEN after {self.failure_count} failures")

# Usage
circuit_breaker = CircuitBreaker()

def protected_completion(model, messages):
    return circuit_breaker.call(litellm.completion, model=model, messages=messages)
```

### 3. Comprehensive Logging and Monitoring

```python
import logging
import time
from functools import wraps

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_completion(func):
    """Decorator to monitor LiteLLM completion calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        model = kwargs.get('model', 'unknown')
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            # Log success
            logger.info(f"SUCCESS: Model={model}, Duration={duration:.2f}s")
            
            # Optional: Send metrics to monitoring system
            # send_metric('litellm.completion.success', 1, tags={'model': model})
            # send_metric('litellm.completion.duration', duration, tags={'model': model})
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            error_type = type(e).__name__
            
            # Log error with context
            logger.error(f"ERROR: Model={model}, Type={error_type}, "
                        f"Duration={duration:.2f}s, Message={str(e)}")
            
            # Optional: Send error metrics
            # send_metric('litellm.completion.error', 1, 
            #            tags={'model': model, 'error_type': error_type})
            
            raise
    
    return wrapper

# Usage
@monitor_completion
def monitored_completion(model, messages):
    return litellm.completion(model=model, messages=messages)
```

### 4. Error Context Preservation

```python
import traceback
from contextlib import contextmanager

@contextmanager
def error_context(context_info):
    """Add context to errors for better debugging."""
    try:
        yield
    except Exception as e:
        # Enhance error with context
        error_msg = f"Context: {context_info}\nOriginal error: {str(e)}"
        
        # Log full context
        logger.error(f"Error with context: {context_info}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Re-raise with enhanced message
        e.args = (error_msg,) + e.args[1:] if e.args else (error_msg,)
        raise

# Usage
def completion_with_context(model, messages, user_id=None, session_id=None):
    context = {
        'model': model,
        'user_id': user_id,
        'session_id': session_id,
        'message_count': len(messages)
    }
    
    with error_context(context):
        return litellm.completion(model=model, messages=messages)
```

## Testing Error Scenarios

```python
import pytest
import litellm
import openai

class TestLiteLLMErrorHandling:
    
    def test_authentication_error(self):
        """Test handling of invalid API keys."""
        with pytest.raises((litellm.AuthenticationError, openai.AuthenticationError)):
            litellm.completion(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                api_key="invalid-key-12345"
            )
    
    def test_bad_request_error(self):
        """Test handling of invalid model names."""
        with pytest.raises((litellm.BadRequestError, openai.BadRequestError)):
            litellm.completion(
                model="definitely-not-a-real-model",
                messages=[{"role": "user", "content": "test"}]
            )
    
    def test_function_calling_support_check(self):
        """Test function calling support detection."""
        # Models that support function calling
        assert litellm.supports_function_calling("gpt-3.5-turbo") == True
        assert litellm.supports_function_calling("gpt-4") == True
        
        # Models that don't support function calling
        assert litellm.supports_function_calling("gpt-3.5-turbo-instruct") == False
    
    def test_retry_logic(self):
        """Test retry logic with mock failures."""
        call_count = 0
        
        def failing_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise litellm.RateLimitError("Rate limited", "", "", "")
            return "success"
        
        # Should succeed after retries
        result = retry_with_backoff(failing_function, max_retries=3, base_delay=0.1)
        assert result == "success"
        assert call_count == 3

# Mock testing for development
def create_mock_litellm_error(error_type, message="Test error", status_code=400):
    """Create mock LiteLLM errors for testing."""
    error = error_type(message, "", "", "")
    error.status_code = status_code
    error.llm_provider = "test_provider"
    return error

# Example usage in tests
def test_error_handling_with_mocks():
    mock_error = create_mock_litellm_error(litellm.RateLimitError, status_code=429)
    
    # Test your error handling logic
    try:
        raise mock_error
    except litellm.RateLimitError as e:
        assert e.status_code == 429
        assert e.llm_provider == "test_provider"
```

## Common Pitfalls and Solutions

### 1. Status Code Type Issues

**Problem:** Some LiteLLM exceptions have `status_code` as empty string instead of integer.

**Solution:**
```python
def safe_should_retry(error):
    """Safely check if error should be retried."""
    try:
        if hasattr(error, 'status_code') and isinstance(error.status_code, int):
            return litellm._should_retry(error.status_code)
    except (TypeError, AttributeError):
        pass
    
    # Fallback logic based on error type
    retryable_types = (
        litellm.RateLimitError,
        litellm.APIConnectionError, 
        litellm.InternalServerError,
        openai.APITimeoutError
    )
    return isinstance(error, retryable_types)
```

### 2. Mixed Exception Sources

**Problem:** Exceptions can come from either `litellm` or `openai` packages.

**Solution:**
```python
def handle_mixed_exceptions(func, *args, **kwargs):
    """Handle exceptions from both litellm and openai sources."""
    try:
        return func(*args, **kwargs)
    except (litellm.AuthenticationError, openai.AuthenticationError):
        print("Authentication failed - check your API key")
    except (litellm.RateLimitError, openai.RateLimitError):
        print("Rate limited - implement backoff")
    except (litellm.BadRequestError, openai.BadRequestError):
        print("Bad request - check your parameters")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        raise
```

### 3. Model-Specific Behavior

**Problem:** Different models have different capabilities and API endpoints.

**Solution:**
```python
def smart_completion(model, messages, tools=None):
    """Intelligently handle different model types."""
    
    # Check for completions API models
    completions_models = ["gpt-3.5-turbo-instruct", "davinci-002", "babbage-002"]
    
    if model in completions_models:
        if tools:
            print(f"Warning: {model} doesn't support tools, ignoring tools parameter")
        
        # Convert messages to prompt for completions API
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        return litellm.completion(model=model, prompt=prompt)
    
    # Standard chat completion
    kwargs = {"model": model, "messages": messages}
    
    # Only add tools if model supports them
    if tools and litellm.supports_function_calling(model):
        kwargs["tools"] = tools
    elif tools:
        print(f"Warning: {model} doesn't support function calling, ignoring tools")
    
    return litellm.completion(**kwargs)
```

## Summary Checklist

**Essential Error Handling Practices:**

1. **✅ Always wrap LiteLLM calls in try-except blocks**
2. **✅ Handle both `litellm` and `openai` exception types**
3. **✅ Implement retry logic only for transient errors (429, 5xx, timeouts)**
4. **✅ Check model capabilities before using advanced features**
5. **✅ Use defensive programming for known issues (status_code types)**
6. **✅ Implement graceful degradation with fallback models**
7. **✅ Add comprehensive logging and monitoring**
8. **✅ Test error scenarios thoroughly**
9. **✅ Use modern import patterns (avoid `openai.error`)**
10. **✅ Distinguish between Completions and Chat Completions APIs**

**Key Takeaways for 2025:**

- OpenAI SDK v1.0+ changed import patterns significantly
- LiteLLM maintains compatibility but requires careful exception handling
- Function calling support varies by model - always check first
- Status code handling has known bugs - implement defensive checks
- Circuit breakers and monitoring are essential for production use
- Test your error handling as thoroughly as your happy path

Remember: LiteLLM's OpenAI-compatible exceptions make it easy to write portable error handling code that works across all providers, but staying current with SDK changes is crucial for maintainable code.