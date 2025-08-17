from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def get_llm_response_from_messages(messages):
    response = completion(
        messages=messages,
        model="gemini/gemini-1.5-flash"
    )

    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    messages = []

    system_prompt = """You are a helpful assistant, answer under 30 words."""
    messages.append({"role": "system", "content": system_prompt})

    user_query = "What is the process for handling customer complaints?"
    messages.append({"role": "user", "content": user_query})

    response = get_llm_response_from_messages(messages)
    print("LLM Response:", response)