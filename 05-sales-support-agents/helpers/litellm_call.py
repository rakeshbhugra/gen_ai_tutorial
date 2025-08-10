from litellm import completion
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyCsGl_MjnKvY2Z7Lyf33CZfRaSndyiXLsQ"

messages = [{ "content": "Hello, how are you?","role": "user"}]

response = completion(model="gemini/gemini-1.5-flash", messages=messages)

print(response["choices"][0]["message"]["content"])