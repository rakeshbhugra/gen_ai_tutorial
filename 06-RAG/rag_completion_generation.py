from query_chroma_db import search_documents
from llm_completion import get_llm_response

query = "What are your core principles"
retrived_docs = search_documents(query)

system_prompt = """You are a helpful assistant that answers questions based on the provided context.
If you don't know the answer, say "I don't know".
Use the context to answer the question.
"""

system_prompt += "-"*40
system_prompt += f"\n\nContext:\n{retrived_docs}\n\n"
system_prompt += "-"*40

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": query},
]

llm_response = get_llm_response(messages)

print("LLM Response:", llm_response)
