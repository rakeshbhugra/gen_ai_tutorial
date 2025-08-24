import json

def sum_numbers(a, b):
    """Add two numbers together and return the sum
    
    Parameters
    ----------
    a : float
        The first number to add
    b : float
        The second number to add
        
    Returns
    -------
    float
        The sum of the two numbers
    -------
    """
    return a + b

def multiply_numbers(a, b):
    """Multiply two numbers together and return the product
    
    Parameters
    ----------
    a : float
        The first number to multiply
    b : float
        The second number to multiply
        
    Returns
    -------
    float
        The product of the two numbers
    """
    return a * b
    
def divide_numbers(a, b):
    """Divide two numbers and return the quotient
    
    Parameters
    ----------
    a : float
        The numerator
    b : float
        The denominator
        
    Returns
    -------
    float
        The quotient of the two numbers
    """
    if b == 0:
        return "Error: Division by zero"
    return a / b

functions = [name for name in globals() if callable(globals()[name]) and name not in ("json", "load_dotenv")]

print("Available functions:")
for func in functions:
    print(f"- {func}") 