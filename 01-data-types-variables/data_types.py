# DATA TYPES AND STRING FORMATTING IN PYTHON

# Example 1: F-string formatting (Python 3.6+)
# F-strings provide a readable way to include variables in strings
name = "John"
age = 30

# F-string syntax: f"text {variable} more text"
print(f"My name is {name} and I am {age} years old.")

# Example 2: Type Hints
# Type hints help with code readability and IDE support
# They don't affect runtime behavior but help catch errors
age: int = 4  # Variable 'age' should be an integer

# List with type hint specifying it contains strings
features: list[str] = ["test", "test2", "test3"]

print(f"Features available: {features}")
print(f"Number of features: {len(features)}")

# Example 3: Different ways to format strings
print(f"Using f-string: Hello {name}")
print("Using .format(): Hello {}".format(name))
print("Using % formatting: Hello %s" % name)
