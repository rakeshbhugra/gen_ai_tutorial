# CALCULATOR CONFIGURATION MODULE
# This module demonstrates how to organize constants and configuration variables
# These can be imported and used across different parts of your application

# Application constants
CALCULATOR_VERSION = "1.0.0"
MAX_OPERATIONS = 100
DEFAULT_PRECISION = 2

# Mathematical constants
PI = 3.14159265359
E = 2.71828182846

# Operation limits
MAX_NUMBER_SIZE = 1000000
MIN_NUMBER_SIZE = -1000000

# Configuration settings
ENABLE_LOGGING = True
DEBUG_MODE = False

# Supported operations
SUPPORTED_OPERATIONS = ["add", "subtract", "multiply", "divide"]

# Error messages
ERROR_MESSAGES = {
    "division_by_zero": "Cannot divide by zero!",
    "invalid_operation": "Operation not supported",
    "number_too_large": "Number exceeds maximum size",
    "number_too_small": "Number below minimum size"
}

# Display this when the module is imported
if __name__ == "__main__":
    print("=== Calculator Configuration ===")
    print(f"Version: {CALCULATOR_VERSION}")
    print(f"Max Operations: {MAX_OPERATIONS}")
    print(f"Supported Operations: {SUPPORTED_OPERATIONS}")