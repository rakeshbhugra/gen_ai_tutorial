# 03 - Basic Chatbot

This module introduces AI chatbot development through a structured learning progression. Each subdirectory builds upon the previous, taking you from simple API calls to production-ready chatbot architectures.

## Learning Path

This module is organized into three progressive sections:

### 📞 [01 - Simple API Calls](./01-simple-api-calls/)
**Foundation Level** | *Time: 1-2 hours*

Learn the basics of AI integration:
- Direct API calls to language models
- Basic conversation management
- Message roles and formatting
- Simple error handling

**Start here:** `01_basic_api_call.py`

### 🏗️ [02 - Basic Classes](./02-basic-classes/)
**Intermediate Level** | *Time: 2-3 hours*

Master object-oriented chatbot design:
- Pydantic models for data validation
- Chatbot class architecture
- Method organization and documentation
- Practical usage patterns

**Start here:** `01_data_models.py`

### 🚀 [03 - Advanced Chatbot](./03-advanced-chatbot/)
**Advanced Level** | *Time: 1-2 hours*

Build production-ready applications:
- Advanced Pydantic integration
- Enterprise-grade error handling
- Extensible architecture patterns
- Performance and security considerations

**Start here:** `01_pydantic_chatbot.py`

## What You'll Learn

- **AI Model Integration**: Using LiteLLM to connect with various AI models
- **Object-Oriented Design**: Building chatbot classes with proper structure
- **Conversation Management**: Maintaining chat history and context
- **Error Handling**: Robust error management for production applications
- **Data Validation**: Using Pydantic for type-safe data structures
- **Production Patterns**: Real-world development practices

## Quick Start

Follow this sequence for optimal learning:

1. **Start with API basics:**
   ```bash
   cd 01-simple-api-calls
   python 01_basic_api_call.py
   ```

2. **Learn object-oriented design:**
   ```bash
   cd ../02-basic-classes
   python 01_data_models.py
   ```

3. **Build advanced features:**
   ```bash
   cd ../03-advanced-chatbot
   python 01_pydantic_chatbot.py
   ```

## Learning Progression

```
01-simple-api-calls/     →  Learn AI API fundamentals
    ↓
02-basic-classes/        →  Master OOP and data structures
    ↓
03-advanced-chatbot/     →  Build production-ready systems
```

## Prerequisites

Install required dependencies:

```bash
pip install litellm python-dotenv pydantic
```

Set up your environment variables in `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Key AI Concepts

### Message Roles
- **system**: Sets AI behavior and personality
- **user**: Human input messages
- **assistant**: AI response messages

### Conversation Context
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hello! How can I help you?"},
    {"role": "user", "content": "What's the weather like?"}
]
```

### Model Selection
```python
# Google Gemini
model = "gemini/gemini-1.5-flash"

# OpenAI GPT
model = "openai/gpt-3.5-turbo" 

# Local Ollama
model = "ollama/llama3:latest"
```

## Design Patterns Demonstrated

1. **Progressive Complexity**: From simple scripts to full classes
2. **Separation of Concerns**: Data models, business logic, and UI separated
3. **Error Handling**: Graceful failure handling at multiple levels
4. **Type Safety**: Using modern Python typing features
5. **Extensibility**: Design allows for easy feature additions

## Best Practices Covered

1. **API Key Security**: Never hardcode API keys
2. **Input Validation**: Validate all user inputs
3. **Error Messaging**: Provide helpful error messages to users
4. **Code Organization**: Logical file and class structure
5. **Documentation**: Comprehensive docstrings and comments
6. **Testing**: Built-in examples and test patterns

## Common Chatbot Patterns

### Basic Chat Loop
```python
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chatbot.get_response(user_input)
    print(f"AI: {response}")
```

### Error Handling
```python
try:
    response = chatbot.get_response(query)
except ValueError as e:
    print(f"Input error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### System Message Setup
```python
chatbot = Chatbot("gemini/gemini-1.5-flash")
chatbot.add_system_message("You are an expert Python tutor.")
```

## Integration with AI Providers

This module demonstrates integration with:
- **Google Gemini**: Fast, cost-effective models
- **OpenAI GPT**: Industry-standard models
- **Anthropic Claude**: Advanced reasoning capabilities
- **Local Models**: Ollama for privacy and control

## Next Steps

Master these chatbot concepts to prepare for **04-streamlit-chatbot**, where we'll build web-based interfaces with modern UI frameworks!

## Troubleshooting

Common issues and solutions:
- **API Key Errors**: Check `.env` file and variable names
- **Import Errors**: Ensure all packages are installed
- **Model Access**: Verify API key permissions for chosen models
- **Rate Limits**: Implement proper retry logic for production use