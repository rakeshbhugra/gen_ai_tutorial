import litellm
import json
from dotenv import load_dotenv

load_dotenv()

def sum_numbers(a, b):
    """Add two numbers together and return the sum
    
    Parameters
    ----------
    a : float
        The first number to add
    b : float
        The second number to add
        
    Returns
    -------
    float
        The sum of the two numbers
    -------
    """
    return a + b

def multiply_numbers(a, b):
    """Multiply two numbers together and return the product
    
    Parameters
    ----------
    a : float
        The first number to multiply
    b : float
        The second number to multiply
        
    Returns
    -------
    float
        The product of the two numbers
    """
    return a * b
    
def divide_numbers(a, b):
    """Divide two numbers and return the quotient
    
    Parameters
    ----------
    a : float
        The numerator
    b : float
        The denominator
        
    Returns
    -------
    float
        The quotient of the two numbers
    """
    if b == 0:
        return "Error: Division by zero"
    return a / b

function_map = {
    "sum_numbers": sum_numbers,
    "multiply_numbers": multiply_numbers,
    "divide_numbers": divide_numbers
}

tools = [
    {"type":"function", "function": litellm.utils.function_to_dict(sum_numbers)},
    {"type":"function", "function": litellm.utils.function_to_dict(multiply_numbers)},
    {"type":"function", "function": litellm.utils.function_to_dict(divide_numbers)},
]

# for tool in tools:
#     print(json.dumps(tool, indent=2))
#     print("-"*40)

conversation_history = []

system_prompt = "You are a helpful assistant that can perform basic arithmetic operations like addition, multiplication, and division. Always use these tools to perform calculations"

conversation_history.append({"role": "system", "content": system_prompt})

user_query = input("User: ")
# user_query = "Add 5 and 7 then multiply the result by 3."

conversation_history.append({"role": "user", "content": user_query})

# model = "openai/gpt-4.1-mini"
model = "gemini/gemini-2.5-flash-lite"

while True:
    response = litellm.completion(
        model=model,
        messages=conversation_history,
        tools=tools,
        tool_choice="auto"
    )

    print("response:", response)
    if len(response.choices) == 0:
        exit("No response from the model")
    response_message = response.choices[0].message
    # print(f"Model response: {response_message}")

    if response_message.tool_calls:

        conversation_history.append({
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": response_message.tool_calls
        })
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            # print(f"\nFunction called: {function_name}")
            # print(f"Arguments: {function_args}")

            if function_name in function_map:
                result = function_map[function_name](**function_args)
                # print(f"Function result: {result}")

                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

            else:
                raise ValueError(f"Function {function_name} not found in function_map")
            
        final_response = litellm.completion(
            model=model,
            messages=conversation_history
        ) 
        conversation_history.append({
            "role": "assistant",
            "content": final_response.choices[0].message.content
        })
        print(f"\nFinal response:\n------\n {final_response.choices[0].message.content}")
                
    else:
        conversation_history.append({
            "role": "assistant",
            "content": response_message.content   
        })
        print(response_message.content)
        
        # new_input = input("User: ")
        # conversation_history.append({"role": "user", "content": new_input})

    with open("tool_calling_conversation_history.json", "w") as f:
        json.dump(conversation_history, f, indent=2)