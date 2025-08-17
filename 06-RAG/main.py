from helper import add_document_to_chromadb, find_similar_chunks
from llm_helper import get_llm_response_from_messages

# take query input
# create query embedding
# Find similar chunks using vector search in our chromadb collection
# Augment the system prompt
# Get response from the LLM

def augment_system_prompt_with_chunks(similar_chunks, messages, user_query):
    system_prompt = """You are a support assistant for the company Capabl. Answer the user's query based on the search results from the company support guide."""

    # Add similar chunks to messages
    system_prompt += "\n\nHere are some relevant sections from the support guide:"
    for chunk in similar_chunks:
        system_prompt += f"\n\n{chunk}"

    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_query})

    return messages

if __name__ == "__main__":
    document_path = "data_files/Capabl Sales Playbook.docx"
    document_name = "Sales Guide"
    add_document_to_chromadb(document_path, document_name)

    # query = input("Enter your query: ")
    query = "What is Mission & Vision of Capabl?"

    # Retrieval
    similar_chunks = find_similar_chunks(query)

    print("Similar chunks found:")
    # for chunk in similar_chunks:
    #     print(f" - {chunk}...")
    #     print("-" * 40)

    messages = []
        
    # Augment the system prompt
    messages = augment_system_prompt_with_chunks(similar_chunks, messages, query)

    # Generate response from LLM
    response = get_llm_response_from_messages(messages)
    print("LLM Response:", response)