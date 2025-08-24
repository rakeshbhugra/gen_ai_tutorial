import litellm
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

function_map = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
    "divide_numbers": divide_numbers
}

tools = [
    {"type":"function", "function": litellm.utils.function_to_dict(sum_numbers)},
    {"type":"function", "function": litellm.utils.function_to_dict(multiply_numbers)},
    {"type":"function", "function": litellm.utils.function_to_dict(divide_numbers)},
]

for tool in tools:
    print(json.dumps(tool, indent=2))
    print("-"*40)

conversation_history = []

system_prompt = "You are "