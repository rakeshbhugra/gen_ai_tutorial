from litellm import completion
from dotenv import load_dotenv

load_dotenv()

messages = [{ "content": "Hello, how are you?","role": "user"}]

response = completion(model="gemini/gemini-2.5-flash-lite", messages=messages)

print(response["choices"][0]["message"]["content"])