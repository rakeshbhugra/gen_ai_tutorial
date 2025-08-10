# CONDITIONAL STATEMENTS IN PYTHON
# Conditional statements allow us to make decisions in our code based on certain conditions

# Example 1: Basic if-else statement
user_message: str = "What is the capital of France?"

# Check if the user message is not empty
if user_message != "":
    print("user is allowed to send this message")
else:
    print("user is not allowed to send this message")

# Example 2: if-elif-else chain
# This demonstrates how multiple conditions are checked in sequence    
if "johnn" == "john":  # This will be False
    print("first condition is true")
elif "john" == "john":  # This will be True, so this block executes
    print("second condition is true")
else:
    print("both conditions are false")

# Example 3: String comparison with case sensitivity
name1 = "John"
name2 = "john"

# Direct comparison - case sensitive
if name1 != name2:
    print("Names are not equal")

# Example 4: Complex conditional logic with logical operators
# Demonstrates AND (and), OR (or) operators and string methods
if name1 == name2 and name1.lower() == name2.lower():
    print("First or second condition is true")
elif name1.lower() == name2.lower() and name1.upper() == name2.upper():
    print("Second condition is true")
elif name1.upper() == name2.upper():  # This condition will be True
    print("Third condition is true")
elif name1.title() == name2.title():
    print("Fourth condition is true")
else:
    print("Both conditions are false")

# String methods used above:
# .lower() - converts string to lowercase
# .upper() - converts string to uppercase  
# .title() - converts string to title case (first letter capitalized)

# Example 5: String validation using built-in methods
text_var = "123a"
print(text_var.isnumeric())  # Returns False because 'a' is not numeric
