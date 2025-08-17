from helper import add_document_to_chromadb
from embeddings_helper import create_embeddings
from chromadb_helper import setup_chromadb
from llm_helper import get_llm_response_from_messages

# take query input
# create query embedding
# Find similar chunks using vector search in our chromadb collection
# Augment the system prompt
# Get response from the LLM

def find_similar_chunks(query):
    # create query embedding
    embeddings = create_embeddings(query)['embedding']

    # Find similar chunks using vector search in our chromadb collection
    _, collection = setup_chromadb()
    results = collection.query(
        query_embeddings=[embeddings],
        n_results=2
    )

    return [x for x in results['documents'][0]]
    

if __name__ == "__main__":
    document_path = "data_files/Capabl Customer Support Guide.docx"
    document_name = "Support Guide"
    # add_document_to_chromadb(document_path, document_name)

    # query = input("Enter your query: ")
    query = "What is the process for handling customer complaints?"
    similar_chunks = find_similar_chunks(query)

    print("Similar chunks found:")
    # for chunk in similar_chunks:
    #     print(f" - {chunk}...")
    #     print("-" * 40)

    messages = []
        
    # Augment the system prompt
    system_prompt = "You are support assistant for the company Capabl. Answer the user's query based on the search results from the company support guide."
    # Add similar chunks to messages
    system_prompt += "\n\nHere are some relevant sections from the support guide:"
    for chunk in similar_chunks:
        system_prompt += f"\n\n{chunk}"

    messages.append({"role": "system", "content": system_prompt})

    # Add user query to messages
    messages.append({"role": "user", "content": query})

    response = get_llm_response_from_messages(messages)
    print("LLM Response:", response)