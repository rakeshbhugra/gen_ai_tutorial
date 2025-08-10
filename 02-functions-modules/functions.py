# MODULE IMPORTS AND USAGE DEMONSTRATION
# This file shows how to import and use functions from different modules

# Example 1: Importing specific functions from modules
# Note: These imports assume the modules exist in the expected locations
try:
    # Import functions from the some_other_name module (renamed for clarity)
    from some_other_name import greet_user, send_email
    print("Successfully imported functions from some_other_name module")
except ImportError as e:
    print(f"Could not import from some_other_name: {e}")

# Example 2: Importing variables from local calculator module
from calculator.summations_helper import add_numbers
from calculator.config import CALCULATOR_VERSION, MAX_OPERATIONS

print(f"Calculator Version: {CALCULATOR_VERSION}")
print(f"Max Operations: {MAX_OPERATIONS}")

# Example 3: Using imported functions
print("\n=== Testing Imported Functions ===")

# Test the calculator function
result = add_numbers(5, 11)
print(f"5 + 11 = {result}")

# Test with different numbers
result2 = add_numbers(100, 25)
print(f"100 + 25 = {result2}")

# Example 4: Different import styles
# Import entire module
import calculator.summations_helper as calc

# Use functions from the imported module
print(f"Using calc.add_numbers(3, 7) = {calc.add_numbers(3, 7)}")
print(f"Using calc.subtract_numbers(10, 4) = {calc.subtract_numbers(10, 4)}")

# Example 5: Importing configuration constants
from calculator.config import PI, E, SUPPORTED_OPERATIONS
print(f"\nMath constants: PI = {PI}, E = {E}")
print(f"Supported operations: {SUPPORTED_OPERATIONS}")

# Example 7: Best practices for imports
"""
IMPORT BEST PRACTICES:
1. Import standard library modules first
2. Import third-party packages second  
3. Import local application modules last
4. Use specific imports when possible: from module import function
5. Use module aliases for long module names: import long_module_name as lmn
6. Avoid wildcard imports: from module import * (except in specific cases)
"""

print("\n=== Module Import Examples Complete ===")