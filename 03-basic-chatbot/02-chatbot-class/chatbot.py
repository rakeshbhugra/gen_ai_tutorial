# COMPREHENSIVE CHATBOT CLASS WITH AI INTEGRATION
# This file demonstrates a complete chatbot implementation using object-oriented programming
# It integrates with AI models through LiteLLM and manages conversation state

from litellm import completion
from dotenv import load_dotenv
import os
from typing import List, Dict, Any

# Load environment variables from .env file
# This is where API keys and configuration should be stored
load_dotenv()

# OBJECT-ORIENTED PROGRAMMING PRIMER
'''
CLASS VS OBJECT - FUNDAMENTAL CONCEPTS:

Class: A blueprint or template that defines the structure and behavior of objects
Object/Instance: A specific entity created from that blueprint with actual data

Real-world analogies:

1. House Blueprint → Your Actual House
   - Blueprint (Class): Defines rooms, layout, materials
   - House (Object): Specific house at 123 Main St with your furniture

2. Cake Recipe → Actual Cake
   - Recipe (Class): Instructions for ingredients and steps
   - Cake (Object): The delicious cake you baked following that recipe

3. Car Specifications → Physical Car
   - Specifications (Class): Engine type, dimensions, features
   - Car (Object): Your specific red Tesla Model S with license plate XYZ123

In programming terms:
- Class defines attributes (data) and methods (functions) that objects will have
- Object is a specific instance with actual values for those attributes
'''

# EXAMPLE CAR CLASS (Educational Purpose)
# This demonstrates basic class concepts before we build our chatbot

# class Car:
#     """Example class showing basic OOP concepts"""
#     def __init__(self, name: str, color: str, brand: str, year: int):
#         """Constructor - called when creating a new Car object"""
#         self.name = name      # Instance attribute
#         self.color = color    # Instance attribute  
#         self.brand = brand    # Instance attribute
#         self.year = year      # Instance attribute

#     def create(self):
#         """Method to display car creation info"""
#         print(f"Creating a car: {self.name}, Color: {self.color}, Brand: {self.brand}, Year: {self.year}")

#     def get_cars_year(self):
#         """Method to display car year"""
#         print(f"Car Year: {self.year}")

#     def get_cars_name(self):
#         """Method to display car name"""
#         print(f"Car Name: {self.name}")

# # Creating objects (instances) from the Car class
# car = Car("Model S", "Red", "Tesla", 2020)
# car.get_cars_year()  # Calls method on car object

# car2 = Car("Mustang", "Blue", "Ford", 2021) 
# car2.get_cars_name()  # Calls method on car2 object

# MAIN CHATBOT CLASS IMPLEMENTATION

class Chatbot:
    """
    A comprehensive chatbot class that manages AI conversations
    
    This class encapsulates all the functionality needed for an AI chatbot:
    - Managing conversation history
    - Validating user input
    - Integrating with AI models via LiteLLM
    - Error handling and recovery
    """
    
    def __init__(self, model_name: str):
        """
        Initialize a new Chatbot instance
        
        Args:
            model_name (str): The AI model identifier (e.g., "gemini/gemini-1.5-flash")
            
        Example:
            chatbot = Chatbot("gemini/gemini-1.5-flash")
        """
        self.model_name = model_name
        # Message history stores the entire conversation
        # Each message is a dictionary with 'role' and 'content' keys
        self.message_history: List[Dict[str, str]] = []
    
    def get_model_name(self) -> None:
        """
        Display the current model name
        Useful for debugging and verification
        """
        print(f"Model Name: {self.model_name}")

    def add_message_to_history(self, message: str, sender: str) -> None:
        """
        Add a message to the conversation history with validation
        
        Args:
            message (str): The message content
            sender (str): The message sender ('user', 'assistant', or 'system')
            
        Raises:
            ValueError: If message is None, empty, or only whitespace
            
        Note:
            This method validates input to ensure message quality
            Empty or whitespace-only messages are rejected
        """
        # Input validation - critical for robust applications
        if message is None or message.strip() == "":
            raise ValueError("message cannot be empty")
        
        # Create message object following OpenAI/LiteLLM format
        message_obj = {
            'role': sender,     # 'user', 'assistant', or 'system'
            'content': message  # The actual message text
        }
        
        # Add to conversation history
        self.message_history.append(message_obj)

    def get_ai_response(self, user_query: str) -> str:
        """
        Get an AI response for the user's query
        
        This is the main method that:
        1. Adds user query to conversation history
        2. Calls the AI model with full conversation context
        3. Processes the AI response
        4. Adds AI response to conversation history
        5. Returns the AI response text
        
        Args:
            user_query (str): The user's input message
            
        Returns:
            str: The AI's response text
            
        Raises:
            ValueError: If user_query is invalid
            Exception: If AI API call fails
        """
        # Step 1: Add user message to history (with validation)
        self.add_message_to_history(user_query, 'user')
        
        try:
            # Step 2: Make API call to AI model
            # Send entire conversation history for context
            response = completion(
                model=self.model_name,      # AI model to use
                messages=self.message_history  # Full conversation context
            )
            
            # Step 3: Extract AI response from API response
            # LiteLLM follows OpenAI response format
            ai_message = response['choices'][0]['message']['content']
            
            # Step 4: Add AI response to conversation history
            self.add_message_to_history(ai_message, 'assistant')
            
            # Step 5: Return response to caller
            return ai_message
            
        except Exception as e:
            # Handle API errors gracefully
            error_message = f"AI service error: {str(e)}"
            # Log the error but don't add to history
            print(f"Error calling AI model: {e}")
            raise Exception(error_message)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get a copy of the conversation history
        
        Returns:
            List[Dict[str, str]]: Copy of the message history
        """
        return self.message_history.copy()
    
    def clear_history(self) -> None:
        """
        Clear the conversation history
        Useful for starting fresh conversations
        """
        self.message_history.clear()
    
    def add_system_message(self, system_prompt: str) -> None:
        """
        Add a system message to set AI behavior/personality
        
        Args:
            system_prompt (str): Instructions for the AI's behavior
            
        Example:
            chatbot.add_system_message("You are a helpful coding assistant.")
        """
        self.add_message_to_history(system_prompt, 'system')

# USAGE EXAMPLE (commented out for module import)
# if __name__ == "__main__":
#     # Create chatbot instance
#     bot = Chatbot("gemini/gemini-1.5-flash")
#     
#     # Set system behavior
#     bot.add_system_message("You are a helpful and friendly assistant.")
#     
#     # Test conversation
#     response = bot.get_ai_response("Hello! How are you?")
#     print(f"AI: {response}")
