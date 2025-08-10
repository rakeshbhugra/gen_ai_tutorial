# CALCULATOR MODULE - MATHEMATICAL OPERATIONS
# This module provides basic mathematical operations that can be imported by other files

def add_numbers(a: float, b: float) -> float:
    """
    Adds two numbers together
    
    Args:
        a (float): First number to add
        b (float): Second number to add
        
    Returns:
        float: Sum of a and b
        
    Example:
        >>> add_numbers(5, 3)
        8
        >>> add_numbers(2.5, 1.5)
        4.0
    """
    return a + b

def subtract_numbers(a: float, b: float) -> float:
    """
    Subtracts the second number from the first number
    
    Args:
        a (float): Number to subtract from
        b (float): Number to subtract
        
    Returns:
        float: Result of a - b
        
    Example:
        >>> subtract_numbers(10, 3)
        7
        >>> subtract_numbers(5.5, 2.5)
        3.0
    """
    return a - b

def multiply_numbers(a: float, b: float) -> float:
    """
    Multiplies two numbers together
    
    Args:
        a (float): First number to multiply
        b (float): Second number to multiply
        
    Returns:
        float: Product of a and b
    """
    return a * b

def divide_numbers(a: float, b: float) -> float:
    """
    Divides the first number by the second number
    
    Args:
        a (float): Dividend (number to be divided)
        b (float): Divisor (number to divide by)
        
    Returns:
        float: Result of a / b
        
    Raises:
        ValueError: If b is zero (division by zero)
    """
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

# Example usage and testing
if __name__ == "__main__":
    # This code only runs when the file is executed directly,
    # not when imported as a module
    print("=== Calculator Module Tests ===")
    
    print(f"5 + 3 = {add_numbers(5, 3)}")
    print(f"10 - 4 = {subtract_numbers(10, 4)}")
    print(f"6 * 7 = {multiply_numbers(6, 7)}")
    print(f"15 / 3 = {divide_numbers(15, 3)}")
    
    # Test with floats
    print(f"2.5 + 1.5 = {add_numbers(2.5, 1.5)}")
    print(f"5.5 - 2.3 = {subtract_numbers(5.5, 2.3)}")
    
    # Test error handling
    try:
        result = divide_numbers(10, 0)
    except ValueError as e:
        print(f"Error: {e}")
