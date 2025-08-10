# DATA MODELS FOR CHATBOT MESSAGES
# This file demonstrates Pydantic models for structured data and basic Python classes
# It shows how to create type-safe data structures for AI applications

from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class ChatMessage(BaseModel):
    """
    Pydantic model for chat messages with validation and type safety
    
    Pydantic automatically validates data types and provides helpful error messages
    when invalid data is passed to the model
    """
    # Literal type restricts role to only these three values
    role: Literal['user', 'assistant', 'system']
    content: str  # The actual message text
    timestamp: datetime = datetime.now()  # Automatically set to current time

# OBJECT-ORIENTED PROGRAMMING CONCEPTS
'''
CLASS VS OBJECT EXPLANATION:

Class: A blueprint or template for creating objects
Object: A specific instance created from that blueprint

Real-world examples:
- Class = blueprint for a house    →  Object = your actual house built from that blueprint
- Class = recipe for a cake        →  Object = the actual cake made from that recipe
- Class = car manufacturing specs  →  Object = a specific car built from those specs

In programming:
- Class defines what attributes and methods objects will have
- Object is a specific instance with actual values for those attributes
'''

class Car:
    """
    Example class to demonstrate basic OOP concepts
    This is a simple blueprint for creating car objects
    """
    def __init__(self, model: str, year: int, color: str):
        """
        Constructor method - called when creating a new Car object
        
        Args:
            model (str): The car model name (e.g., "Tesla Model 3")
            year (int): Manufacturing year
            color (str): Car color
        """
        # Instance attributes - each car object will have its own values
        self.model = model
        self.year = year
        self.color = color
    
    def get_info(self) -> str:
        """Return formatted information about this car"""
        return f"{self.year} {self.color} {self.model}"
    
    def is_vintage(self) -> bool:
        """Check if the car is considered vintage (over 25 years old)"""
        current_year = datetime.now().year
        return (current_year - self.year) > 25

# UNDERSTANDING 'self' IN PYTHON
'''
WHAT IS 'self'?

'self' is a reference to the current instance of the class. It's Python's way of allowing
methods to access and modify the attributes of the specific object they're called on.

Key points about 'self':
1. It's the first parameter in instance methods
2. It allows access to instance attributes (self.attribute_name)
3. It distinguishes between instance variables and local variables
4. Python automatically passes the object as 'self' when you call a method

Example:
    car1 = Car("Honda", 2020, "Red")
    car2 = Car("Toyota", 2018, "Blue")
    
    car1.get_info()  # Python automatically passes car1 as 'self'
    car2.get_info()  # Python automatically passes car2 as 'self'
'''

class ChatBot:
    """
    Simple chatbot class that manages conversation history using ChatMessage objects
    This demonstrates how to use Pydantic models within regular Python classes
    """
    def __init__(self, model_name: str = "gemini-pro"):
        """
        Initialize a new chatbot instance
        
        Args:
            model_name (str): Name of the AI model to use
        """
        self.model_name = model_name
        # Type hint specifies this is a list containing ChatMessage objects
        self.conversation_history: list[ChatMessage] = []
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a new message to the conversation history
        
        Args:
            role (str): Message role ('user', 'assistant', or 'system')
            content (str): The message text
            
        The ChatMessage model will automatically validate the role and content
        """
        # Create a new ChatMessage object with validation
        message = ChatMessage(role=role, content=content)
        # Add it to our conversation history
        self.conversation_history.append(message)
    
    def get_conversation_length(self) -> int:
        """Return the number of messages in the conversation"""
        return len(self.conversation_history)
    
    def get_last_message(self) -> ChatMessage | None:
        """Return the most recent message, or None if no messages exist"""
        if self.conversation_history:
            return self.conversation_history[-1]
        return None

# EXAMPLE USAGE AND TESTING
if __name__ == "__main__":
    print("=== Testing ChatMessage Model ===")
    
    # Create a chat message
    msg = ChatMessage(role="user", content="Hello, world!")
    print(f"Message: {msg.content}")
    print(f"Role: {msg.role}")
    print(f"Timestamp: {msg.timestamp}")
    
    print("\n=== Testing Car Class ===")
    
    # Create car objects
    car1 = Car("Tesla Model 3", 2023, "White")
    car2 = Car("Ford Mustang", 1995, "Red")
    
    print(f"Car 1: {car1.get_info()}")
    print(f"Car 2: {car2.get_info()}")
    print(f"Is car1 vintage? {car1.is_vintage()}")
    print(f"Is car2 vintage? {car2.is_vintage()}")
    
    print("\n=== Testing ChatBot Class ===")
    
    # Create a chatbot
    bot = ChatBot("gpt-4")
    
    # Add some messages
    bot.add_message("system", "You are a helpful assistant")
    bot.add_message("user", "What is Python?")
    bot.add_message("assistant", "Python is a programming language")
    
    print(f"Conversation length: {bot.get_conversation_length()}")
    print(f"Last message: {bot.get_last_message().content}")