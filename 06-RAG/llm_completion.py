from litellm import completion
from dotenv import load_dotenv
load_dotenv()

def get_llm_response(messages, model="gemini/gemini-1.5-flash"):
    response = completion(
        model=model,
        messages=messages,
    )
    return response['choices'][0]['message']['content']