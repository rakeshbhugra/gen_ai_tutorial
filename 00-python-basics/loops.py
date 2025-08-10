# LOOPS IN PYTHON
# Loops allow us to repeat code multiple times efficiently

# Example 1: Basic range() function usage
# Uncomment the lines below to see different ways to use range()

# Simple way to print numbers 1-10
# print('1,2,3,4,5,6,7,8,9,10')

# Using a for loop with range() to print numbers 1-100
# range(start, stop) - generates numbers from start to stop-1
# for i in range(1, 101):
#     print(i, end=', ')  # end=', ' prevents newline and adds comma

# Print numbers from 1 to 10 using a loop
# range(1, 11) generates numbers: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
# Note: 1 <= number < 11

# for i in range(1, 11):
#     print(i)

# Example 2: Working with lists and loops
items = ["1", True, 3.13]  # A list containing different data types

# Adding items to a list
# items.append("new item")

# Method 1: Iterating directly over items
# for item in items:
#     print(item)

# Method 2: Using enumerate() to get both index and value
# enumerate() returns pairs of (index, value)
# for idx, item in enumerate(items):
#     print(f"{idx}: {item}")

# Method 3: Using range() with list indexing
# This is useful when you need to access items by their position
for i in range(0, 3):  # range(0, 3) gives us: 0, 1, 2
    print(f"{i}: {items[i]}")  # Access list item using index

# Getting the length of a list
print(f"The list has {len(items)} items")

# LOOP TYPES SUMMARY:
# 1. for loop - iterate over sequences (lists, strings, ranges)
# 2. while loop - repeat while a condition is True
# 3. range() - generate sequences of numbers
# 4. enumerate() - get both index and value when iterating
