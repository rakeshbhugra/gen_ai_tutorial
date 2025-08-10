# VARIABLE NAMING CONVENTIONS IN PYTHON

# Example 1: Standard variable naming
name1 = "jason"  # Lowercase with descriptive name

# Example 2: Private/internal variables
# Variables starting with underscore are considered "private" by convention
# They won't be imported when using "from module import *"
_secret = 52  # Private variable - indicates internal use only

# Example 3: Different naming conventions
user_name = "alice"      # snake_case (recommended for Python)
userName = "bob"         # camelCase (less common in Python)
USER_NAME = "charlie"    # UPPER_CASE (typically for constants)

# Example 4: Valid variable names
age = 25
user_2 = "second_user"
is_valid = True
total_count = 100

# Example 5: Invalid variable names (commented out to avoid errors)
# 2age = 25           # Can't start with number
# user-name = "test"  # Can't contain hyphens
# class = "MyClass"   # Can't use Python keywords

print(f"Name 1: {name1}")
print(f"Secret value: {_secret}")
print(f"User name (snake_case): {user_name}")
print(f"User name (camelCase): {userName}")
print(f"USER NAME (UPPER_CASE): {USER_NAME}")

# Example 6: Best practices for variable naming
# - Use descriptive names
# - Use snake_case for variables and functions
# - Use UPPER_CASE for constants
# - Use leading underscore for private variables
# - Avoid single character names except for loop counters

MAXIMUM_RETRIES = 3      # Constant
current_user_id = 1001   # Descriptive variable name
_internal_counter = 0    # Private variable