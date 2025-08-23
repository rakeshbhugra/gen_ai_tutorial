"""
LiteLLM Error Handling Tutorial (Simple Version)

This module provides a clean, simple interface for learning about
LiteLLM error handling by importing demonstrations from organized modules.

The error demonstrations are split into separate files for better organization:
- error_demonstrations.py: Individual error type demos
- litellm_error_handling_refactored.py: Advanced patterns and utilities
"""

# Import all error demonstrations
from error_demonstrations import (
    demonstrate_authentication_error,
    demonstrate_bad_request_error,
    demonstrate_unsupported_tool_error,
    demonstrate_error_information_extraction,
    demonstrate_all_errors
)

# Import advanced error handling utilities
from litellm_error_handling_refactored import (
    retry_with_exponential_backoff,
    robust_completion,
    ErrorHandler
)

def quick_demo():
    """Run a quick demonstration of key error types."""
    print("🚨 LiteLLM Error Handling - Quick Demo 🚨\n")
    
    # Demo key error types
    demonstrate_authentication_error()
    demonstrate_bad_request_error()
    demonstrate_unsupported_tool_error()
    demonstrate_error_information_extraction()
    
    print("✨ For more comprehensive demos, run:")
    print("   python error_demonstrations.py")
    print("   python litellm_error_handling_refactored.py")

def show_best_practices():
    """Show error handling best practices."""
    print("\n📚 Error Handling Best Practices:\n")
    
    practices = [
        "1. Always wrap LiteLLM calls in try-except blocks",
        "2. Handle different error types appropriately:",
        "   - AuthenticationError: Fix credentials (don't retry)",
        "   - BadRequestError: Fix request parameters (don't retry)",
        "   - RateLimitError: Retry with exponential backoff",
        "   - APITimeoutError: Increase timeout or retry",
        "   - InternalServerError: May indicate unsupported features",
        "3. Use litellm.supports_function_calling() before using tools",
        "4. Implement circuit breakers for resilience",
        "5. Track error statistics for monitoring",
        "6. Extract error details for better debugging"
    ]
    
    for practice in practices:
        print(f"   {practice}")
    
    print("\n💡 Code Example:")
    print("""
    try:
        if litellm.supports_function_calling(model):
            response = litellm.completion(model=model, tools=tools, ...)
        else:
            response = litellm.completion(model=model, messages=messages)
    except litellm.AuthenticationError:
        # Fix API keys
    except litellm.BadRequestError:
        # Fix request parameters
    except litellm.RateLimitError:
        # Retry with backoff
    except litellm.InternalServerError as e:
        if "tools" in str(e):
            # Model doesn't support tools
    """)

def main():
    """Main function to demonstrate error handling."""
    print("🛡️ LiteLLM Error Handling Tutorial 🛡️\n")
    
    print("This tutorial is organized into modular components:")
    print("📁 error_demonstrations.py - Individual error type demos")
    print("📁 litellm_error_handling_refactored.py - Advanced patterns")
    print("📁 litellm_error_handling_simple.py - This file (overview)")
    
    print("\n" + "="*50 + "\n")
    
    # Run quick demo
    quick_demo()
    
    # Show best practices
    show_best_practices()
    
    print("\n🎉 Tutorial complete!")
    print("\nNext steps:")
    print("- Run the individual demo files for detailed examples")
    print("- Implement error handling in your own LiteLLM applications")
    print("- Use the ErrorHandler class for centralized error management")

if __name__ == "__main__":
    main()