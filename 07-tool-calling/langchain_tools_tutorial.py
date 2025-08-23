"""
LangChain Tools Tutorial - The Easy Way to Do Function Calling

This demonstrates how much simpler tool calling is with LangChain
compared to raw LiteLLM. LangChain handles all the complex schema
generation and tool execution automatically.
"""

from langchain_core.tools import tool
from langchain_community.chat_models import ChatLiteLLM
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import json

load_dotenv()

# ================================
# 1. BASIC TOOL DEFINITION
# ================================

@tool
def sum_numbers(a: float, b: float) -> float:
    """Add two numbers together and return the sum.
    
    Args:
        a: The first number to add
        b: The second number to add
    
    Returns:
        The sum of the two numbers
    """
    return a + b

@tool  
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together and return the product.
    
    Args:
        a: The first number to multiply
        b: The second number to multiply
    
    Returns:
        The product of the two numbers
    """
    return a * b

@tool
def calculate_circle_area(radius: float) -> float:
    """Calculate the area of a circle given its radius.
    
    Args:
        radius: The radius of the circle
        
    Returns:
        The area of the circle (π * r²)
    """
    import math
    return math.pi * radius ** 2

@tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get current weather for a location (mock implementation).
    
    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: Temperature unit - either 'fahrenheit' or 'celsius'
        
    Returns:
        A description of the current weather
    """
    # Mock weather data
    temp = 72 if unit == "fahrenheit" else 22
    return f"Weather in {location}: {temp}°{unit[0].upper()}, sunny with light breeze"

# ================================
# 2. ADVANCED TOOLS
# ================================

@tool
def search_contacts(name: str) -> str:
    """Search for a contact by name in the address book.
    
    Args:
        name: The name to search for
        
    Returns:
        Contact information if found
    """
    # Mock contact database
    contacts = {
        "alice": {"phone": "555-0123", "email": "alice@email.com"},
        "bob": {"phone": "555-0456", "email": "bob@email.com"},
        "charlie": {"phone": "555-0789", "email": "charlie@email.com"}
    }
    
    name_lower = name.lower()
    if name_lower in contacts:
        contact = contacts[name_lower]
        return f"Found {name}: Phone: {contact['phone']}, Email: {contact['email']}"
    else:
        return f"No contact found for '{name}'"

@tool
def create_reminder(task: str, date: str) -> str:
    """Create a reminder for a specific task and date.
    
    Args:
        task: The task to be reminded about
        date: The date for the reminder (e.g., "2024-12-25")
        
    Returns:
        Confirmation message
    """
    return f"✅ Reminder created: '{task}' on {date}"

@tool
def analyze_text_sentiment(text: str) -> str:
    """Analyze the sentiment of given text (mock implementation).
    
    Args:
        text: The text to analyze
        
    Returns:
        Sentiment analysis result
    """
    # Simple mock sentiment analysis
    positive_words = ["good", "great", "excellent", "amazing", "wonderful", "happy", "love"]
    negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "disappointed"]
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return f"Sentiment: Positive (positive words: {pos_count}, negative: {neg_count})"
    elif neg_count > pos_count:
        return f"Sentiment: Negative (positive words: {pos_count}, negative: {neg_count})"
    else:
        return f"Sentiment: Neutral (positive words: {pos_count}, negative: {neg_count})"

# ================================
# 3. SIMPLE TOOL BINDING APPROACH
# ================================

def simple_tool_binding_demo():
    """Demonstrate simple tool binding without agents"""
    print("=== Simple Tool Binding Demo ===\n")
    
    # Initialize model
    model = ChatLiteLLM(model="gemini/gemini-2.5-flash-lite")
    
    # Bind tools to model - this is where the magic happens!
    tools = [sum_numbers, multiply_numbers, calculate_circle_area]
    model_with_tools = model.bind_tools(tools)
    
    test_cases = [
        "What is 25 + 37?",
        "Calculate 8 times 12",
        "What's the area of a circle with radius 5?",
        "Hello, how are you today?"  # No tool needed
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case}")
        
        try:
            # Single call - LangChain handles tool detection
            response = model_with_tools.invoke([HumanMessage(content=test_case)])
            
            # Check if model wants to call tools
            if response.tool_calls:
                print("🔧 Tool calls detected:")
                for tool_call in response.tool_calls:
                    print(f"   - {tool_call['name']} with args: {tool_call['args']}")
                    
                    # Execute tool manually
                    tool_name = tool_call['name']
                    if tool_name == 'sum_numbers':
                        result = sum_numbers.invoke(tool_call['args'])
                    elif tool_name == 'multiply_numbers':
                        result = multiply_numbers.invoke(tool_call['args'])
                    elif tool_name == 'calculate_circle_area':
                        result = calculate_circle_area.invoke(tool_call['args'])
                    
                    print(f"   ✅ Result: {result}")
            else:
                print(f"💬 Direct response: {response.content}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()

# ================================
# 4. AGENT-BASED APPROACH (AUTOMATIC)
# ================================

def agent_based_demo():
    """Demonstrate automatic tool execution with agents"""
    print("=== Agent-Based Demo (Automatic Tool Execution) ===\n")
    
    try:
        # Initialize model
        model = ChatLiteLLM(model="gemini/gemini-2.5-flash-lite")
        
        # Define all available tools
        tools = [
            sum_numbers, 
            multiply_numbers, 
            calculate_circle_area,
            get_weather,
            search_contacts,
            create_reminder,
            analyze_text_sentiment
        ]
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant with access to various tools. Use them when needed to answer questions accurately."),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        # Create agent - this handles everything automatically!
        agent = create_tool_calling_agent(model, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        # Test cases that require different tools
        test_cases = [
            "What is 15 + 27?",
            "Calculate the area of a circle with radius 10",
            "What's the weather like in New York?",
            "Find contact information for Alice",
            "Create a reminder to call mom on 2024-12-25",
            "Analyze the sentiment of this text: 'I love this amazing product!'",
            "What's 5 times 8, and also what's the weather in Tokyo?",  # Multiple tools
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*50}")
            print(f"Test {i}: {test_case}")
            print('='*50)
            
            try:
                # Agent automatically handles tool calling!
                result = agent_executor.invoke({"input": test_case})
                print(f"\n🎯 Final Answer: {result['output']}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except ImportError as e:
        print("❌ Missing dependencies for agents:")
        print("   Run: pip install langchain langchain-community")
        print(f"   Error: {e}")

# ================================
# 5. TOOL INSPECTION
# ================================

def inspect_tools():
    """Show how LangChain automatically generates tool schemas"""
    print("=== Tool Schema Inspection ===\n")
    
    # Show how @tool decorator automatically creates schemas
    print("🔍 Automatically generated tool schema for sum_numbers:")
    print(json.dumps(sum_numbers.args, indent=2))
    
    print(f"\n📝 Tool name: {sum_numbers.name}")
    print(f"📝 Tool description: {sum_numbers.description}")
    
    print("\n🔍 Schema for calculate_circle_area:")
    print(json.dumps(calculate_circle_area.args, indent=2))
    
    print("\n🔍 All available tools:")
    tools = [sum_numbers, multiply_numbers, calculate_circle_area, get_weather, search_contacts]
    for tool in tools:
        print(f"   - {tool.name}: {tool.description}")

# ================================
# 6. COMPARISON WITH RAW LITELLM
# ================================

def compare_with_raw_litellm():
    """Compare LangChain tools with raw LiteLLM approach"""
    print("=== LangChain vs Raw LiteLLM Comparison ===\n")
    
    print("📊 Code Complexity Comparison:")
    print("\n🔧 LangChain Approach:")
    print("```python")
    print("@tool")
    print("def sum_numbers(a: float, b: float) -> float:")
    print('    """Add two numbers together."""')
    print("    return a + b")
    print("")
    print("model = ChatLiteLLM(model='gpt-3.5-turbo')")
    print("model_with_tools = model.bind_tools([sum_numbers])")
    print("response = model_with_tools.invoke('What is 2 + 3?')")
    print("```")
    
    print("\n⚙️ Raw LiteLLM Approach:")
    print("```python")
    print("def sum_numbers(a, b):")
    print("    return a + b")
    print("")
    print("tools = [{")
    print('    "type": "function",')
    print('    "function": {')
    print('        "name": "sum_numbers",')
    print('        "description": "Add two numbers together",')
    print('        "parameters": {')
    print('            "type": "object",')
    print('            "properties": {')
    print('                "a": {"type": "number", "description": "First number"},')
    print('                "b": {"type": "number", "description": "Second number"}')
    print('            },')
    print('            "required": ["a", "b"]')
    print('        }')
    print('    }')
    print("}]")
    print("")
    print("response = litellm.completion(")
    print("    model='gpt-3.5-turbo',")
    print("    messages=[...],")
    print("    tools=tools")
    print(")")
    print("# + manual tool execution logic...")
    print("```")
    
    print("\n📈 Benefits of LangChain Tools:")
    print("   ✅ Automatic schema generation from docstrings")
    print("   ✅ Type safety with Python type hints")
    print("   ✅ Automatic tool execution (with agents)")
    print("   ✅ Built-in error handling")
    print("   ✅ Much less boilerplate code")
    print("   ✅ Consistent interface across providers")

# ================================
# 7. ERROR HANDLING WITH LANGCHAIN
# ================================

def error_handling_demo():
    """Demonstrate error handling with LangChain tools"""
    print("=== Error Handling with LangChain Tools ===\n")
    
    @tool
    def divide_numbers(a: float, b: float) -> float:
        """Divide two numbers.
        
        Args:
            a: The dividend
            b: The divisor
            
        Returns:
            The result of a divided by b
        """
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b
    
    # Test error handling
    print("🧪 Testing divide by zero:")
    try:
        result = divide_numbers.invoke({"a": 10, "b": 0})
        print(f"Result: {result}")
    except ValueError as e:
        print(f"❌ Caught error: {e}")
        print("💡 LangChain tools can raise and handle Python exceptions normally")
    
    print("\n🧪 Testing successful division:")
    try:
        result = divide_numbers.invoke({"a": 10, "b": 2})
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all demonstrations"""
    print("🚀 LangChain Tools Tutorial 🚀\n")
    
    inspect_tools()
    print("\n" + "="*60 + "\n")
    
    simple_tool_binding_demo()
    print("="*60 + "\n")
    
    agent_based_demo()
    print("\n" + "="*60 + "\n")
    
    error_handling_demo()
    print("\n" + "="*60 + "\n")
    
    compare_with_raw_litellm()
    
    print("\n🎉 Tutorial Complete!")
    print("\n💡 Key Takeaways:")
    print("   1. @tool decorator automatically generates schemas")
    print("   2. bind_tools() attaches tools to models")
    print("   3. Agents automatically execute tools")
    print("   4. Much simpler than raw LiteLLM function calling")
    print("   5. Built-in error handling and type safety")
    print("   6. Works across all LLM providers")

if __name__ == "__main__":
    main()