"""
Comprehensive LiteLLM Error Handling Implementation
Includes: Retry logic, fallback models, circuit breaker, rate limiting,
structured logging, metrics collection, and graceful degradation.
"""

import time
import logging
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import random
import hashlib
from functools import wraps

import litellm
from litellm import completion
from litellm.exceptions import (
    AuthenticationError,
    InvalidRequestError,
    RateLimitError,
    ServiceUnavailableError,
    Timeout,
    APIConnectionError,
    APIError
)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure LiteLLM logging
litellm.set_verbose = False  # Set to True for debugging


class ModelTier(Enum):
    """Model tiers for fallback strategy"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    FALLBACK = "fallback"


@dataclass
class ModelConfig:
    """Configuration for a model"""
    name: str
    tier: ModelTier
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    timeout: int = 30
    cost_per_1k_tokens: float = 0.0


@dataclass
class CircuitBreakerState:
    """State for circuit breaker pattern"""
    failure_count: int = 0
    last_failure_time: Optional[datetime] = None
    state: str = "closed"  # closed, open, half-open
    success_count: int = 0
    half_open_start: Optional[datetime] = None


@dataclass
class Metrics:
    """Metrics collection for monitoring"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    retries: int = 0
    fallback_used: int = 0
    total_latency: float = 0.0
    errors_by_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    requests_by_model: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    rate_limit_hits: int = 0
    circuit_breaker_trips: int = 0


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()
    
    def is_allowed(self) -> bool:
        """Check if request is allowed"""
        now = datetime.now()
        
        # Remove old requests outside the window
        while self.requests and self.requests[0] < now - timedelta(seconds=self.window_seconds):
            self.requests.popleft()
        
        # Check if we can make a request
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
    
    def wait_time(self) -> float:
        """Calculate wait time until next request is allowed"""
        if len(self.requests) < self.max_requests:
            return 0
        
        oldest_request = self.requests[0]
        now = datetime.now()
        wait_time = (oldest_request + timedelta(seconds=self.window_seconds) - now).total_seconds()
        return max(0, wait_time)


class ComprehensiveErrorHandler:
    """Comprehensive error handling for LLM completions"""
    
    def __init__(
        self,
        models: List[ModelConfig],
        max_retries: int = 3,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: int = 60,
        rate_limiter_config: Optional[Dict[str, int]] = None
    ):
        self.models = sorted(models, key=lambda x: x.tier.value)
        self.max_retries = max_retries
        self.circuit_breakers = {model.name: CircuitBreakerState() for model in models}
        self.circuit_breaker_threshold = circuit_breaker_threshold
        self.circuit_breaker_timeout = circuit_breaker_timeout
        self.metrics = Metrics()
        
        # Initialize rate limiter
        rate_config = rate_limiter_config or {"max_requests": 10, "window_seconds": 60}
        self.rate_limiter = RateLimiter(**rate_config)
        
        # Request ID for tracing
        self.request_counter = 0
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID for tracing"""
        self.request_counter += 1
        timestamp = datetime.now().isoformat()
        return hashlib.md5(f"{timestamp}_{self.request_counter}".encode()).hexdigest()[:8]
    
    def _log_with_context(
        self,
        level: str,
        message: str,
        request_id: str,
        model: Optional[str] = None,
        **kwargs
    ):
        """Structured logging with context"""
        context = {
            "request_id": request_id,
            "model": model,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        log_message = f"[{request_id}] {message} | Context: {json.dumps(context)}"
        getattr(logger, level)(log_message)
    
    def _check_circuit_breaker(self, model_name: str) -> bool:
        """Check if circuit breaker allows the request"""
        cb = self.circuit_breakers[model_name]
        now = datetime.now()
        
        if cb.state == "closed":
            return True
        
        elif cb.state == "open":
            # Check if timeout has passed
            if cb.last_failure_time and \
               now - cb.last_failure_time > timedelta(seconds=self.circuit_breaker_timeout):
                # Move to half-open state
                cb.state = "half-open"
                cb.half_open_start = now
                cb.success_count = 0
                self._log_with_context(
                    "info",
                    f"Circuit breaker entering half-open state",
                    request_id="CB",
                    model=model_name
                )
                return True
            return False
        
        elif cb.state == "half-open":
            # Allow limited requests in half-open state
            return cb.success_count < 3
        
        return False
    
    def _update_circuit_breaker(self, model_name: str, success: bool):
        """Update circuit breaker state based on request outcome"""
        cb = self.circuit_breakers[model_name]
        
        if success:
            if cb.state == "half-open":
                cb.success_count += 1
                if cb.success_count >= 3:
                    # Close the circuit
                    cb.state = "closed"
                    cb.failure_count = 0
                    cb.success_count = 0
                    self._log_with_context(
                        "info",
                        "Circuit breaker closed after successful recovery",
                        request_id="CB",
                        model=model_name
                    )
            elif cb.state == "closed":
                cb.failure_count = 0
        else:
            cb.failure_count += 1
            cb.last_failure_time = datetime.now()
            
            if cb.state == "half-open" or cb.failure_count >= self.circuit_breaker_threshold:
                # Open the circuit
                cb.state = "open"
                self.metrics.circuit_breaker_trips += 1
                self._log_with_context(
                    "warning",
                    f"Circuit breaker opened after {cb.failure_count} failures",
                    request_id="CB",
                    model=model_name
                )
    
    def _handle_rate_limit(self, request_id: str, wait_time: float = None):
        """Handle rate limiting with exponential backoff"""
        self.metrics.rate_limit_hits += 1
        
        if wait_time is None:
            # Calculate wait time with jitter
            base_wait = 2 ** min(self.metrics.rate_limit_hits, 6)  # Cap at 64 seconds
            wait_time = base_wait + random.uniform(0, 1)
        
        self._log_with_context(
            "warning",
            f"Rate limit hit, waiting {wait_time:.2f} seconds",
            request_id=request_id,
            rate_limit_hits=self.metrics.rate_limit_hits
        )
        
        time.sleep(wait_time)
    
    def _execute_completion(
        self,
        model_config: ModelConfig,
        messages: List[Dict],
        request_id: str,
        **kwargs
    ) -> Optional[Any]:
        """Execute a single completion request with error handling"""
        
        # Check circuit breaker
        if not self._check_circuit_breaker(model_config.name):
            self._log_with_context(
                "warning",
                "Circuit breaker is open, skipping model",
                request_id=request_id,
                model=model_config.name
            )
            return None
        
        # Check rate limiter
        if not self.rate_limiter.is_allowed():
            wait_time = self.rate_limiter.wait_time()
            self._handle_rate_limit(request_id, wait_time)
        
        attempt = 0
        last_error = None
        
        while attempt < self.max_retries:
            attempt += 1
            
            try:
                self._log_with_context(
                    "info",
                    f"Attempting completion (attempt {attempt}/{self.max_retries})",
                    request_id=request_id,
                    model=model_config.name,
                    attempt=attempt
                )
                
                # Prepare kwargs with model-specific settings
                completion_kwargs = {
                    "model": model_config.name,
                    "messages": messages,
                    "timeout": model_config.timeout,
                    **kwargs
                }
                
                if model_config.max_tokens:
                    completion_kwargs["max_tokens"] = model_config.max_tokens
                if model_config.temperature is not None:
                    completion_kwargs["temperature"] = model_config.temperature
                
                # Execute completion
                start_time = time.time()
                response = completion(**completion_kwargs)
                latency = time.time() - start_time
                
                # Update metrics
                self.metrics.successful_requests += 1
                self.metrics.total_latency += latency
                self.metrics.requests_by_model[model_config.name] += 1
                
                # Update circuit breaker
                self._update_circuit_breaker(model_config.name, success=True)
                
                self._log_with_context(
                    "info",
                    f"Completion successful",
                    request_id=request_id,
                    model=model_config.name,
                    latency=latency,
                    attempt=attempt
                )
                
                return response
                
            except RateLimitError as e:
                last_error = e
                self.metrics.errors_by_type["RateLimitError"] += 1
                
                # Extract wait time from error if available
                wait_time = getattr(e, 'retry_after', None)
                self._handle_rate_limit(request_id, wait_time)
                
            except AuthenticationError as e:
                # Non-retryable error
                last_error = e
                self.metrics.errors_by_type["AuthenticationError"] += 1
                self._log_with_context(
                    "error",
                    f"Authentication failed: {str(e)}",
                    request_id=request_id,
                    model=model_config.name
                )
                self._update_circuit_breaker(model_config.name, success=False)
                break
                
            except InvalidRequestError as e:
                # Non-retryable error
                last_error = e
                self.metrics.errors_by_type["InvalidRequestError"] += 1
                self._log_with_context(
                    "error",
                    f"Invalid request: {str(e)}",
                    request_id=request_id,
                    model=model_config.name
                )
                break
                
            except (ServiceUnavailableError, APIConnectionError, Timeout) as e:
                # Retryable errors
                last_error = e
                error_type = type(e).__name__
                self.metrics.errors_by_type[error_type] += 1
                self.metrics.retries += 1
                
                # Exponential backoff with jitter
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                self._log_with_context(
                    "warning",
                    f"Retryable error: {str(e)}, waiting {wait_time:.2f}s",
                    request_id=request_id,
                    model=model_config.name,
                    error_type=error_type,
                    attempt=attempt
                )
                
                if attempt < self.max_retries:
                    time.sleep(wait_time)
                
            except Exception as e:
                # Unexpected error
                last_error = e
                self.metrics.errors_by_type["UnexpectedError"] += 1
                self._log_with_context(
                    "error",
                    f"Unexpected error: {str(e)}",
                    request_id=request_id,
                    model=model_config.name,
                    error_type=type(e).__name__
                )
                break
        
        # All retries exhausted
        self._update_circuit_breaker(model_config.name, success=False)
        return None
    
    def complete_with_fallback(
        self,
        messages: List[Dict],
        **kwargs
    ) -> Optional[Any]:
        """Execute completion with fallback models"""
        request_id = self._generate_request_id()
        self.metrics.total_requests += 1
        
        self._log_with_context(
            "info",
            "Starting completion request",
            request_id=request_id,
            num_models=len(self.models)
        )
        
        last_error = None
        
        for i, model_config in enumerate(self.models):
            try:
                if i > 0:
                    self.metrics.fallback_used += 1
                    self._log_with_context(
                        "info",
                        f"Attempting fallback model {i+1}/{len(self.models)}",
                        request_id=request_id,
                        model=model_config.name,
                        tier=model_config.tier.value
                    )
                
                response = self._execute_completion(
                    model_config,
                    messages,
                    request_id,
                    **kwargs
                )
                
                if response:
                    return response
                    
            except Exception as e:
                last_error = e
                self._log_with_context(
                    "error",
                    f"Model failed: {str(e)}",
                    request_id=request_id,
                    model=model_config.name
                )
        
        # All models failed
        self.metrics.failed_requests += 1
        self._log_with_context(
            "error",
            "All models failed, returning None",
            request_id=request_id,
            models_tried=len(self.models)
        )
        
        return None
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of collected metrics"""
        success_rate = (
            self.metrics.successful_requests / self.metrics.total_requests * 100
            if self.metrics.total_requests > 0 else 0
        )
        
        avg_latency = (
            self.metrics.total_latency / self.metrics.successful_requests
            if self.metrics.successful_requests > 0 else 0
        )
        
        return {
            "total_requests": self.metrics.total_requests,
            "successful_requests": self.metrics.successful_requests,
            "failed_requests": self.metrics.failed_requests,
            "success_rate": f"{success_rate:.2f}%",
            "average_latency": f"{avg_latency:.2f}s",
            "retries": self.metrics.retries,
            "fallback_used": self.metrics.fallback_used,
            "rate_limit_hits": self.metrics.rate_limit_hits,
            "circuit_breaker_trips": self.metrics.circuit_breaker_trips,
            "errors_by_type": dict(self.metrics.errors_by_type),
            "requests_by_model": dict(self.metrics.requests_by_model)
        }
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = Metrics()
        logger.info("Metrics reset")


def create_default_handler() -> ComprehensiveErrorHandler:
    """Create a handler with default configuration"""
    models = [
        ModelConfig(
            name="gpt-4",
            tier=ModelTier.PRIMARY,
            max_tokens=4096,
            temperature=0.7,
            timeout=30,
            cost_per_1k_tokens=0.03
        ),
        ModelConfig(
            name="gpt-3.5-turbo",
            tier=ModelTier.SECONDARY,
            max_tokens=4096,
            temperature=0.7,
            timeout=20,
            cost_per_1k_tokens=0.002
        ),
        ModelConfig(
            name="claude-3-haiku-20240307",
            tier=ModelTier.FALLBACK,
            max_tokens=4096,
            temperature=0.7,
            timeout=20,
            cost_per_1k_tokens=0.00025
        )
    ]
    
    return ComprehensiveErrorHandler(
        models=models,
        max_retries=3,
        circuit_breaker_threshold=5,
        circuit_breaker_timeout=60,
        rate_limiter_config={"max_requests": 10, "window_seconds": 60}
    )


# Decorator for easy integration
def with_comprehensive_error_handling(
    handler: Optional[ComprehensiveErrorHandler] = None,
    **handler_kwargs
):
    """Decorator to add comprehensive error handling to any function"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal handler
            if handler is None:
                handler = create_default_handler()
            
            # Extract messages from function arguments
            messages = kwargs.get("messages") or (args[0] if args else None)
            if not messages:
                raise ValueError("Messages parameter is required")
            
            # Remove messages from kwargs to avoid duplication
            completion_kwargs = {k: v for k, v in kwargs.items() if k != "messages"}
            
            return handler.complete_with_fallback(messages, **completion_kwargs)
        
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    # Initialize handler with custom configuration
    handler = ComprehensiveErrorHandler(
        models=[
            ModelConfig("gpt-4", ModelTier.PRIMARY, timeout=30),
            ModelConfig("gpt-3.5-turbo", ModelTier.SECONDARY, timeout=20),
            ModelConfig("claude-3-haiku-20240307", ModelTier.FALLBACK, timeout=15)
        ],
        max_retries=3,
        circuit_breaker_threshold=5,
        circuit_breaker_timeout=60
    )
    
    # Example 1: Direct usage
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    response = handler.complete_with_fallback(messages)
    
    if response:
        print(f"Response: {response.choices[0].message.content}")
    else:
        print("All attempts failed")
    
    # Example 2: Using decorator
    @with_comprehensive_error_handling()
    def get_completion(messages, temperature=0.7):
        # This function is automatically wrapped with error handling
        pass
    
    response = get_completion(messages, temperature=0.5)
    
    # Print metrics summary
    print("\nMetrics Summary:")
    print(json.dumps(handler.get_metrics_summary(), indent=2))
    
    # Example 3: Simulating various error scenarios
    def simulate_error_scenarios():
        """Simulate various error conditions for testing"""
        
        # Test with invalid model to trigger fallback
        test_handler = ComprehensiveErrorHandler(
            models=[
                ModelConfig("invalid-model", ModelTier.PRIMARY, timeout=5),
                ModelConfig("gpt-3.5-turbo", ModelTier.SECONDARY, timeout=20)
            ],
            max_retries=2
        )
        
        messages = [{"role": "user", "content": "Test message"}]
        
        print("\n=== Testing Error Scenarios ===")
        
        # Scenario 1: Primary model fails, fallback succeeds
        response = test_handler.complete_with_fallback(messages)
        print(f"Scenario 1 - Fallback test: {'Success' if response else 'Failed'}")
        
        # Scenario 2: Rate limiting
        print("\nScenario 2 - Rate limiting test:")
        for i in range(3):
            response = test_handler.complete_with_fallback(messages)
            print(f"  Request {i+1}: {'Success' if response else 'Failed'}")
        
        # Print final metrics
        print("\n=== Final Metrics ===")
        print(json.dumps(test_handler.get_metrics_summary(), indent=2))
    
    # Uncomment to run error scenario simulation
    # simulate_error_scenarios()