from litellm import completion
import os
from dotenv import load_dotenv

load_dotenv()

messages = [{ "content": "Hello, how are you?","role": "user"}]

response = completion(model="gemini/gemini-1.5-flash", messages=messages)

print(response["choices"][0]["message"]["content"])