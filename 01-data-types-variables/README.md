# 01 - Data Types & Variables

This module introduces Python's type system, variable naming conventions, and string formatting techniques essential for AI development.

## What You'll Learn

- **Python Data Types**: Understanding Python's built-in data types
- **Type Hints**: Modern Python type annotation syntax
- **Variable Naming**: Best practices for naming variables and constants
- **String Formatting**: Multiple ways to format strings in Python

## Files in This Module

### 1. `01_data_types.py`
Comprehensive guide to Python data types with type hints:
- **Basic Types**: `str`, `int`, `bool`, `float`
- **Collection Types**: `list`, `dict`, `tuple`
- **Type Hints**: Modern Python type annotation syntax
- **Function Annotations**: Typed function parameters and return values

**Key Concepts:**
- Understanding Python's dynamic typing vs type hints
- Using `type()` to inspect variable types
- Writing type-safe functions
- Documentation with docstrings

### 2. `data_types.py`
Focuses on string formatting and f-strings:
- **F-string Syntax**: Modern string formatting (Python 3.6+)
- **Variable Interpolation**: Embedding variables in strings
- **Alternative Formatting**: `.format()` and `%` formatting methods
- **Type Hints for Collections**: `list[str]` syntax

**Key Concepts:**
- F-string expressions and formatting options
- Comparing different string formatting approaches
- Type hints for better code documentation

### 3. `variables/names.py`
Python variable naming conventions and best practices:
- **Naming Conventions**: snake_case, camelCase, UPPER_CASE
- **Private Variables**: Using underscore prefix convention
- **Valid vs Invalid**: Python identifier rules
- **Best Practices**: Descriptive naming and constants

**Key Concepts:**
- PEP 8 style guide compliance
- Public vs private variable conventions
- Constants and their naming patterns

## Running the Code

Execute any of these files to see the concepts in action:

```bash
python 01_data_types.py
python data_types.py
python variables/names.py
```

## Key Takeaways

1. **Type Hints**: Use type annotations for better code documentation and IDE support
2. **F-strings**: Prefer f-string formatting for readability and performance
3. **Naming**: Follow snake_case for variables, UPPER_CASE for constants
4. **Private Variables**: Use underscore prefix to indicate internal use

## Practical Exercises

1. **Type Exploration**: Create variables of each major type and print their types
2. **String Formatting**: Practice f-strings with different data types
3. **Naming Practice**: Refactor poorly named variables to follow conventions
4. **Type Hints**: Add type hints to existing functions

## Connection to AI Development

These concepts are crucial for AI applications:
- **Type Safety**: Prevents common errors in data processing pipelines
- **String Formatting**: Essential for prompt engineering and output formatting
- **Variable Organization**: Critical for managing model parameters and configurations

## Next Steps

With solid understanding of data types and variables, you're ready for **02-functions-modules** where we'll explore code organization and reusability!