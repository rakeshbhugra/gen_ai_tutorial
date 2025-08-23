from litellm import completion
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

class ClassifyQuery(BaseModel):
    category: Literal["sales", "support", "general"]
    search_query: str

messages = [
    { "role": "system", "content": "You are a helpful assistant that classifies customer queries. Always respond with valid JSON." },
]

query = "I need help with my order status and delivery time."
prompt = f"""
Classify this customer query: "{query}"

Respond with JSON containing:
- category: one of "sales", "support", or "general"
- search_query: keywords for searching knowledge base

JSON format:
"""

messages.append({ "role": "user", "content": prompt })

response = completion(
    model="gpt-4o-mini",
    messages=messages,
    response_format=ClassifyQuery
)

# Extract and parse the JSON response
import json
json_content = response.choices[0].message.content
print("Raw JSON response:")
print(json_content)

# Parse and validate with Pydantic
parsed_data = json.loads(json_content)
classified_query = ClassifyQuery(**parsed_data)

print("\nParsed with Pydantic:")
print(f"Category: {classified_query.category}")
print(f"Search Query: {classified_query.search_query}")