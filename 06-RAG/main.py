from helper import add_document_to_chromadb
from embeddings_helper import create_embeddings
from chromadb_helper import setup_chromadb

# take query input
# create query embedding
# Find similar chunks using vector search in our chromadb collection
# Augment the system prompt
# Get response from the LLM

def find_similar_chunks(embeddings):
    _, collection = setup_chromadb()
    results = collection.query(
        query_embeddings=[embeddings],
        n_results=5
    )
    return [x for x in results['documents'][0]]
    

if __name__ == "__main__":
    document_path = "data_files/Capabl Customer Support Guide.docx"
    document_name = "Support Guide"

    # add_document_to_chromadb(document_path, document_name)

    # query = input("Enter your query: ")
    query = "What is the process for handling customer complaints?"

    # create query embedding
    embeddings = create_embeddings(query)['embedding']

    # Find similar chunks using vector search in our chromadb collection
    similar_chunks = find_similar_chunks(embeddings)
    

    print("Similar chunks found:")
    for chunk in similar_chunks:
        print(f" - {chunk}...")
        print("-" * 40)
