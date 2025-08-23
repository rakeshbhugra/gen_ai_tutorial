# LiteLLM Error Handling Complete Guide

## Overview

LiteLLM maps all provider-specific errors to OpenAI-compatible exceptions, ensuring consistent error handling across different LLM providers (OpenAI, Anthropic, Google, etc.).

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
    ├── APITimeoutError
    └── APIConnectionError (500+)
```

## Error Types and Handling

### 1. AuthenticationError (401)

**When it occurs:**
- Invalid API key
- Expired credentials
- Missing authentication

**Example:**
```python
try:
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except litellm.AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    print(f"Provider: {e.llm_provider}")
    # Don't retry - fix credentials first
```

**Should you retry?** ❌ No - Fix credentials first

### 2. BadRequestError (400)

**When it occurs:**
- Invalid model name
- Context window exceeded
- Malformed request parameters
- Unsupported parameters (but see InternalServerError for tools)

**Example:**
```python
try:
    response = litellm.completion(
        model="gpt-nonexistent",  # Invalid model
        messages=[{"role": "user", "content": "Hello"}]
    )
except litellm.BadRequestError as e:
    print(f"Bad request: {e.message}")
    if "model" in str(e).lower():
        print("Use a valid model name")
    elif "context" in str(e).lower():
        print("Reduce message length")
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
except litellm.PermissionDeniedError as e:
    print(f"Permission denied: {e.message}")
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
except litellm.NotFoundError as e:
    print(f"Not found: {e.message}")
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
try:
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except litellm.RateLimitError as e:
    print(f"Rate limited: {e.message}")
    
    # Check if we should retry
    should_retry = litellm._should_retry(e.status_code)
    if should_retry:
        time.sleep(60)  # Wait before retry
```

**Should you retry?** ✅ Yes - With exponential backoff

### 6. APITimeoutError

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
- **Using tools with models that don't support them** (special case)

**Example:**
```python
try:
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except litellm.APIConnectionError as e:
    print(f"Connection error: {e.message}")
    print(f"Status: {e.status_code}")
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
└── APIConnectionError? → ✅ Retry with backoff
```

## Exponential Backoff Implementation

```python
import time
import random

def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries + 1):
        try:
            return func()
        except (litellm.RateLimitError, litellm.APIConnectionError, openai.APITimeoutError) as e:
            if attempt == max_retries:
                raise e
            
            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"Retrying in {delay:.1f}s...")
            time.sleep(delay)
```

## Error Information Extraction

Every LiteLLM exception provides:

```python
try:
    response = litellm.completion(...)
except litellm.BadRequestError as e:
    # Standard attributes
    print(f"Message: {e.message}")          # Human-readable error
    print(f"Status Code: {e.status_code}")  # HTTP status code
    print(f"Provider: {e.llm_provider}")    # Which provider failed
    
    # OpenAI compatibility
    print(f"Type: {type(e).__name__}")      # Exception type
```

## Function Calling Error Handling

### Special Case: Tools with Unsupported Models

When you try to use tools/functions with models that don't support them, you get **InternalServerError (500)** instead of BadRequestError:

```python
# Models that DON'T support tools (use Completions API)
unsupported_models = [
    "gpt-3.5-turbo-instruct",
    "text-davinci-003",  # Deprecated
    "babbage-002",
    "davinci-002"
]

# This will throw InternalServerError
try:
    response = litellm.completion(
        model="gpt-3.5-turbo-instruct",
        prompt="Calculate 2+2",  # Note: uses 'prompt' not 'messages'
        tools=[...]  # ❌ ERROR: Tools not supported!
    )
except litellm.InternalServerError as e:
    # Error: "Completions.create() got an unexpected keyword argument 'tools'"
    print("Model doesn't support tools!")

# BEST PRACTICE: Always check first
if litellm.supports_function_calling(model):
    # Safe to use tools
    response = litellm.completion(model=model, tools=tools, ...)
else:
    # Use prompt engineering instead
    response = litellm.completion(model=model, prompt=prompt_with_instructions)
```

## Function Calling Error Handling

### Tool Definition Errors

```python
try:
    # Invalid tool schema
    tools = [{"type": "function", "function": {"name": "test"}}]  # Missing parameters
    response = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Use tool"}],
        tools=tools
    )
except litellm.BadRequestError as e:
    if "tool" in str(e).lower():
        print("Invalid tool schema")
        # Fix tool definition
```

### Function Execution Errors

```python
def risky_function(x):
    if x < 0:
        raise ValueError("x must be positive")
    return x * 2

# In your tool execution handler
try:
    result = risky_function(function_args["x"])
except Exception as e:
    # Return error to model
    error_response = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": f"Error: {str(e)}"
    }
    messages.append(error_response)
```

## Best Practices

### 1. Graceful Degradation

```python
def safe_completion(model, messages, fallback_model="gpt-3.5-turbo"):
    try:
        return litellm.completion(model=model, messages=messages)
    except (litellm.NotFoundError, litellm.PermissionDeniedError):
        print(f"Falling back to {fallback_model}")
        return litellm.completion(model=fallback_model, messages=messages)
```

### 2. Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time < self.timeout:
                raise Exception("Circuit breaker is OPEN")
            else:
                self.state = "HALF_OPEN"
        
        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failure_count = 0
        self.state = "CLOSED"
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
```

### 3. Logging and Monitoring

```python
import logging

logger = logging.getLogger(__name__)

def monitored_completion(model, messages):
    try:
        response = litellm.completion(model=model, messages=messages)
        logger.info(f"Success: {model}")
        return response
    except Exception as e:
        logger.error(f"Error: {model} - {type(e).__name__}: {e}")
        # Send to monitoring system
        raise
```

### 4. Error Context Preservation

```python
def completion_with_context(model, messages, context=None):
    try:
        return litellm.completion(model=model, messages=messages)
    except Exception as e:
        # Add context to error for better debugging
        error_msg = f"Context: {context}, Model: {model}, Error: {e}"
        logger.error(error_msg)
        
        # Re-raise with additional context
        e.args = (f"{e.args[0]} (Context: {context})",) + e.args[1:]
        raise
```

## Testing Error Scenarios

```python
import pytest

def test_authentication_error():
    with pytest.raises(litellm.AuthenticationError):
        litellm.completion(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            api_key="invalid"
        )

def test_bad_request_error():
    with pytest.raises(litellm.BadRequestError):
        litellm.completion(
            model="nonexistent-model",
            messages=[{"role": "user", "content": "test"}]
        )
```

## Summary

1. **Always wrap LiteLLM calls in try-except blocks**
2. **Handle different error types appropriately**
3. **Implement retry logic for transient errors only**
4. **Extract error details for debugging**
5. **Use circuit breakers for reliability**
6. **Log errors for monitoring**
7. **Test error scenarios**

Remember: LiteLLM's OpenAI-compatible exceptions make it easy to write portable error handling code that works across all providers!