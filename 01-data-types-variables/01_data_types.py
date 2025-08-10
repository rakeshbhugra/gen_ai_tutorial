# PYTHON DATA TYPES WITH TYPE HINTS
# This file demonstrates Python's main data types and type annotation syntax

# Example 1: String data type
name: str = "Chatbot"  # Type hint indicates this variable holds a string
print(f"Name: {name} (Type: {type(name).__name__})")

# Example 2: Integer data type
age: int = 4  # Type hint indicates this variable holds an integer
print(f"Age: {age} (Type: {type(age).__name__})")

# Example 3: Boolean data type
is_active: bool = True  # Type hint indicates this variable holds a boolean
print(f"Is Active: {is_active} (Type: {type(is_active).__name__})")

# Example 4: List data type
features: list = ["chat", "answer questions", "learn"]  # List can contain any type
print(f"Features: {features} (Type: {type(features).__name__})")

# More specific type hint for list containing only strings
specific_features: list[str] = ["chat", "answer questions", "learn"]
print(f"Specific Features: {specific_features}")

# Example 5: Function with type hints
def validate_input(user_input: str) -> bool:
    """
    Validates user input to ensure it's not empty
    
    Args:
        user_input (str): The input string to validate
        
    Returns:
        bool: True if input is valid, False otherwise
    """
    # Check if input is None or empty string
    if not user_input or len(user_input) == 0:
        return False
    return True

# Test the function
test_input = "Hello World"
result = validate_input(test_input)
print(f"Is '{test_input}' valid? {result}")

# Example 6: Other common data types
price: float = 19.99  # Decimal numbers
items_count: int = 42  # Whole numbers
user_data: dict = {"name": "Alice", "age": 25}  # Key-value pairs
coordinates: tuple = (10.5, 20.3)  # Immutable sequence

print(f"Price: {price} (Type: {type(price).__name__})")
print(f"Items Count: {items_count} (Type: {type(items_count).__name__})")
print(f"User Data: {user_data} (Type: {type(user_data).__name__})")
print(f"Coordinates: {coordinates} (Type: {type(coordinates).__name__})")
