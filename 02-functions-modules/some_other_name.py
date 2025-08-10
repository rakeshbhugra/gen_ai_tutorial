# FUNCTIONS AND TYPE ANNOTATIONS IN PYTHON
# This file demonstrates different types of functions and their usage

from typing import Union, Tuple

# Example 1: Simple function without parameters
def print_hello_world():
    """A basic function that prints hello messages"""
    print("Hello, someone!")  # Fixed typo from "someoneg"
    print("Hello, Earth!")

# Uncomment to test
# print_hello_world()

# Example 2: Function with parameters and type hints
def greet_user(name: str):
    """
    Greets a user with their name
    
    Args:
        name (str): The name of the user to greet
    """
    print(f"Hello, {name}!")

# Uncomment to test
# greet_user("Alice")

# Example 3: Function with multiple parameters and return type annotation
def send_email(name: str, email: str) -> None:
    """
    Simulates sending an email to a user
    
    Args:
        name (str): The recipient's name
        email (str): The recipient's email address
        
    Returns:
        None: This function doesn't return a value
    """
    # Using triple quotes for multi-line strings
    email_template = """Hello {name},
    Thank you for signing up for our service. We are excited to have you on board!
    Best regards,
    The Team
    """
    # Using .format() method for string formatting
    print(email_template.format(name=name))
    print("Email sent to:", email)
    
    return None  # Explicit return (optional for None)

# Example 4: Function that returns a value
def add_numbers(a: int, b: int) -> int:
    """
    Adds two integers and returns the result
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        int: Sum of a and b
    """
    return a + b

# Example 5: Function returning multiple values (tuple unpacking)
def get_user_info() -> Tuple[str, int, str]:
    """
    Returns user information as a tuple
    
    Returns:
        Tuple[str, int, str]: A tuple containing (name, age, email)
    """
    name = "Alice"
    age = 30
    email = "alice@example.com"
    return name, age, email  # Returns a tuple

# Uncomment to test tuple unpacking
# name, age, email = get_user_info()
# print(f"Name: {name}, Age: {age}, Email: {email}")

# Example 6: Function with Union type (accepts multiple types)
def process_id(user_id: Union[int, str]) -> str:
    """
    Processes a user ID that can be either int or string
    
    Args:
        user_id (Union[int, str]): User ID as integer or string
        
    Returns:
        str: Processed ID as string
    """
    return f"User ID: {user_id}"

# Example 7: Function with default parameters
def create_user(name: str, age: int = 18, active: bool = True) -> dict:
    """
    Creates a user dictionary with default values
    
    Args:
        name (str): User's name (required)
        age (int, optional): User's age. Defaults to 18.
        active (bool, optional): User's active status. Defaults to True.
        
    Returns:
        dict: User information dictionary
    """
    return {
        "name": name,
        "age": age,
        "active": active
    }

# Test the functions
if __name__ == "__main__":
    print("=== Function Examples ===")
    
    # Test basic functions
    print_hello_world()
    
    # Test parameterized functions
    greet_user("Bob")
    
    # Test function with return value
    result = add_numbers(5, 3)
    print(f"5 + 3 = {result}")
    
    # Test tuple unpacking
    name, age, email = get_user_info()
    print(f"Name: {name}, Age: {age}, Email: {email}")
    
    # Test union types
    print(process_id(123))
    print(process_id("abc123"))
    
    # Test default parameters
    user1 = create_user("Charlie")
    user2 = create_user("Diana", 25, False)
    print(f"User 1: {user1}")
    print(f"User 2: {user2}")