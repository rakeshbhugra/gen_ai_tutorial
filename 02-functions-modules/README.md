# 02 - Functions & Modules

This module covers Python functions, code organization, and module system - essential skills for building maintainable AI applications.

## What You'll Learn

- **Function Definition**: Creating reusable code blocks
- **Type Annotations**: Modern Python typing for better code quality
- **Module System**: Organizing and importing code
- **Error Handling**: Proper exception management
- **Code Documentation**: Writing clear docstrings

## Files in This Module

### 1. `some_other_name.py`
Comprehensive function examples with modern Python practices:
- **Basic Functions**: Simple functions without parameters
- **Parameterized Functions**: Functions with typed arguments
- **Return Types**: Functions returning values with type hints
- **Multiple Returns**: Tuple unpacking and multiple return values
- **Union Types**: Functions accepting multiple input types
- **Default Parameters**: Optional arguments with default values

**Key Concepts:**
- Function docstrings and documentation
- Type hints with `typing` module
- `if __name__ == "__main__":` pattern
- Error handling with try-catch

### 2. `calculator/summations_helper.py`
Modular calculator implementation demonstrating:
- **Mathematical Operations**: Basic arithmetic functions
- **Error Handling**: Division by zero protection
- **Module Documentation**: Comprehensive function documentation
- **Testing Pattern**: Built-in testing when run directly

**Key Concepts:**
- Creating importable modules
- Function documentation with examples
- Error handling with custom exceptions
- Module testing patterns

### 3. `functions.py`
Module import and usage demonstration:
- **Import Styles**: Different ways to import modules
- **Path Management**: Handling module paths
- **Error Handling**: Graceful import failure handling
- **Best Practices**: Import organization and conventions

**Key Concepts:**
- Relative vs absolute imports
- Module search path (`sys.path`)
- Import best practices and organization
- Cross-directory imports

## Running the Code

Each file can be executed independently:

```bash
# Run function examples
python some_other_name.py

# Test the calculator module
python calculator/summations_helper.py

# Demonstrate module imports
python functions.py
```

## Key Python Concepts

### Function Syntax
```python
def function_name(param: type) -> return_type:
    """Function documentation"""
    return result
```

### Import Patterns
```python
# Specific imports
from module import function

# Module import with alias
import long_module_name as short_name

# Relative imports
from .submodule import function
```

### Type Annotations
```python
from typing import Union, Tuple, List

def process_data(items: List[str]) -> Tuple[int, str]:
    return len(items), items[0]
```

## Best Practices Demonstrated

1. **Type Hints**: Use type annotations for better code clarity
2. **Docstrings**: Document functions with clear descriptions and examples
3. **Error Handling**: Anticipate and handle potential errors gracefully
4. **Module Organization**: Keep related functions together in modules
5. **Testing**: Include test code in modules using `if __name__ == "__main__"`
6. **Import Organization**: Follow PEP 8 import ordering conventions

## Practical Exercises

1. **Function Creation**: Write functions with different parameter patterns
2. **Module Building**: Create your own calculator module with additional operations
3. **Import Practice**: Practice different import styles and error handling
4. **Documentation**: Add comprehensive docstrings to existing functions
5. **Type Safety**: Add type hints to untyped functions

## Connection to AI Development

Functions and modules are crucial for AI applications:
- **Data Processing**: Functions for cleaning and transforming data
- **Model Operations**: Modular code for training and inference
- **API Integration**: Organized code for calling AI services
- **Error Handling**: Robust error management for production systems
- **Code Reusability**: Sharing functions across different AI projects

## Common Patterns in AI Code

```python
# Data processing function
def preprocess_text(text: str) -> List[str]:
    """Clean and tokenize text for AI model input"""
    return text.lower().split()

# Model interface function
def get_ai_response(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Get response from AI model with error handling"""
    try:
        # AI model call logic here
        return response
    except Exception as e:
        raise AIModelError(f"Model call failed: {e}")
```

## Next Steps

With functions and modules mastered, you're ready for **03-basic-chatbot** where we'll apply these concepts to build actual AI chatbot functionality!