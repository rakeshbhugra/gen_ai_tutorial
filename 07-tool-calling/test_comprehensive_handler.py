"""
Test script for comprehensive error handling implementation
Demonstrates various error scenarios and recovery mechanisms
"""

import os
import json
import time
from litellm_comprehensive_error_handling import (
    ComprehensiveErrorHandler,
    ModelConfig,
    ModelTier,
    with_comprehensive_error_handling
)

def test_basic_completion():
    """Test basic completion with fallback"""
    print("\n" + "="*50)
    print("TEST 1: Basic Completion with Fallback")
    print("="*50)
    
    # Configure handler with multiple models
    handler = ComprehensiveErrorHandler(
        models=[
            ModelConfig("gpt-4", ModelTier.PRIMARY, timeout=30),
            ModelConfig("gpt-3.5-turbo", ModelTier.SECONDARY, timeout=20),
            ModelConfig("claude-3-haiku-20240307", ModelTier.FALLBACK, timeout=15)
        ],
        max_retries=2,
        circuit_breaker_threshold=3
    )
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about error handling in Python."}
    ]
    
    response = handler.complete_with_fallback(messages, temperature=0.7)
    
    if response:
        print(f"✅ Success! Response from: {response.model}")
        print(f"Response: {response.choices[0].message.content}")
    else:
        print("❌ All models failed")
    
    print("\nMetrics:")
    print(json.dumps(handler.get_metrics_summary(), indent=2))
    
    return handler


def test_circuit_breaker():
    """Test circuit breaker functionality"""
    print("\n" + "="*50)
    print("TEST 2: Circuit Breaker Pattern")
    print("="*50)
    
    # Use an invalid primary model to trigger circuit breaker
    handler = ComprehensiveErrorHandler(
        models=[
            ModelConfig("invalid-model-xyz", ModelTier.PRIMARY, timeout=5),
            ModelConfig("gpt-3.5-turbo", ModelTier.SECONDARY, timeout=20)
        ],
        max_retries=1,
        circuit_breaker_threshold=2,
        circuit_breaker_timeout=10
    )
    
    messages = [{"role": "user", "content": "Test message"}]
    
    print("Making requests to trigger circuit breaker...")
    for i in range(4):
        print(f"\nRequest {i+1}:")
        response = handler.complete_with_fallback(messages)
        if response:
            print(f"  ✅ Success with {response.model}")
        else:
            print(f"  ⚠️  Request failed, checking circuit breaker state...")
        
        # Check circuit breaker states
        for model_name, cb_state in handler.circuit_breakers.items():
            print(f"  Circuit breaker for {model_name}: {cb_state.state} "
                  f"(failures: {cb_state.failure_count})")
    
    print("\nMetrics after circuit breaker test:")
    print(json.dumps(handler.get_metrics_summary(), indent=2))
    
    return handler


def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\n" + "="*50)
    print("TEST 3: Rate Limiting")
    print("="*50)
    
    # Configure aggressive rate limiting for testing
    handler = ComprehensiveErrorHandler(
        models=[
            ModelConfig("gpt-3.5-turbo", ModelTier.PRIMARY, timeout=20)
        ],
        max_retries=1,
        rate_limiter_config={"max_requests": 2, "window_seconds": 10}
    )
    
    messages = [{"role": "user", "content": "Quick test"}]
    
    print("Making rapid requests to test rate limiting...")
    start_time = time.time()
    
    for i in range(4):
        print(f"\nRequest {i+1} at {time.time() - start_time:.2f}s:")
        response = handler.complete_with_fallback(messages, max_tokens=10)
        if response:
            print(f"  ✅ Success")
        else:
            print(f"  ❌ Failed")
    
    print(f"\nTotal time: {time.time() - start_time:.2f}s")
    print("\nMetrics after rate limiting test:")
    print(json.dumps(handler.get_metrics_summary(), indent=2))
    
    return handler


def test_decorator_usage():
    """Test decorator pattern for easy integration"""
    print("\n" + "="*50)
    print("TEST 4: Decorator Usage")
    print("="*50)
    
    @with_comprehensive_error_handling(
        max_retries=2,
        circuit_breaker_threshold=3
    )
    def get_ai_response(messages, temperature=0.7, max_tokens=100):
        """Function automatically wrapped with error handling"""
        pass
    
    messages = [
        {"role": "user", "content": "What is 2+2? Answer in one word."}
    ]
    
    response = get_ai_response(messages, temperature=0.5, max_tokens=10)
    
    if response:
        print(f"✅ Decorator test successful!")
        print(f"Response: {response.choices[0].message.content}")
    else:
        print("❌ Decorator test failed")
    
    return response


def test_metrics_collection():
    """Test comprehensive metrics collection"""
    print("\n" + "="*50)
    print("TEST 5: Metrics Collection")
    print("="*50)
    
    handler = ComprehensiveErrorHandler(
        models=[
            ModelConfig("gpt-3.5-turbo", ModelTier.PRIMARY, timeout=20),
            ModelConfig("claude-3-haiku-20240307", ModelTier.FALLBACK, timeout=15)
        ],
        max_retries=2
    )
    
    # Make several requests to generate metrics
    test_messages = [
        {"role": "user", "content": "Say 'one'"},
        {"role": "user", "content": "Say 'two'"},
        {"role": "user", "content": "Say 'three'"}
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\nRequest {i}:")
        response = handler.complete_with_fallback([msg], max_tokens=10)
        if response:
            print(f"  ✅ Success")
    
    # Display comprehensive metrics
    print("\n📊 Comprehensive Metrics Summary:")
    metrics = handler.get_metrics_summary()
    
    print(f"  Total Requests: {metrics['total_requests']}")
    print(f"  Success Rate: {metrics['success_rate']}")
    print(f"  Average Latency: {metrics['average_latency']}")
    print(f"  Retries: {metrics['retries']}")
    print(f"  Fallback Used: {metrics['fallback_used']}")
    print(f"  Rate Limit Hits: {metrics['rate_limit_hits']}")
    print(f"  Circuit Breaker Trips: {metrics['circuit_breaker_trips']}")
    
    if metrics['errors_by_type']:
        print(f"\n  Errors by Type:")
        for error_type, count in metrics['errors_by_type'].items():
            print(f"    - {error_type}: {count}")
    
    if metrics['requests_by_model']:
        print(f"\n  Requests by Model:")
        for model, count in metrics['requests_by_model'].items():
            print(f"    - {model}: {count}")
    
    return handler


def main():
    """Run all tests"""
    print("\n" + "🚀 "*20)
    print("COMPREHENSIVE ERROR HANDLING TEST SUITE")
    print("🚀 "*20)
    
    # Check for API keys
    api_keys_present = []
    if os.getenv("OPENAI_API_KEY"):
        api_keys_present.append("OpenAI")
    if os.getenv("ANTHROPIC_API_KEY"):
        api_keys_present.append("Anthropic")
    
    if api_keys_present:
        print(f"\n✅ API Keys found for: {', '.join(api_keys_present)}")
    else:
        print("\n⚠️  No API keys found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables.")
        print("   Tests will attempt to run but may fail without valid credentials.\n")
    
    tests = [
        ("Basic Completion", test_basic_completion),
        ("Circuit Breaker", test_circuit_breaker),
        ("Rate Limiting", test_rate_limiting),
        ("Decorator Pattern", test_decorator_usage),
        ("Metrics Collection", test_metrics_collection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*50}")
            print(f"Running: {test_name}")
            print(f"{'='*50}")
            
            result = test_func()
            results.append((test_name, "✅ PASSED"))
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            results.append((test_name, f"❌ FAILED: {str(e)[:50]}"))
        
        # Small delay between tests
        time.sleep(1)
    
    # Print summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    for test_name, result in results:
        print(f"{test_name}: {result}")
    
    passed = sum(1 for _, r in results if "✅" in r)
    total = len(results)
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed successfully!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")


if __name__ == "__main__":
    main()