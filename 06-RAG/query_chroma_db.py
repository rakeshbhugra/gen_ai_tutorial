from chromadb_helper import setup_chromadb
from embeddings_helper import create_embeddings

# initialize ChromaDB client and collection
client, collection = setup_chromadb()

# query = "How many closed tickets do you review?"
# # create embeddings for the query
# query_embedding = create_embeddings(query)['embedding']

# perform the query on the collection
# results = collection.query(
#     query_embeddings=[query_embedding],
#     n_results=2,
#     include=["documents", "metadatas", "distances"]
# )

# # print the results
# print("Query Results:")
# for i, doc in enumerate(results['documents'][0]):
#     print(f"Result {i + 1}:")
#     print(f"Document: {doc}")
#     print(f"Metadata: {results['metadatas'][0][i]}")
#     print(f"Distance: {results['distances'][0][i]}")
#     print("-" * 40)  # Separator for readability

def search_documents(query, num_results=3):
    """
    Search for documents in the ChromaDB collection based on a query.
    
    Args:
        query (str): The search query.
        num_results (int): The number of results to return.
        
    Returns:
        dict: A dictionary containing the search results.
    """
    query_embedding = create_embeddings(query)['embedding']
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=num_results,
        include=["documents", "metadatas", "distances"]
    )
    return [x for x in results['documents'][0]]

if __name__ == "__main__":
    # Example usage of the search_documents function
    query = "What is the process for handling customer complaints?"
    results = search_documents(query)
    
    print(f"\n=== Query: '{query}' ===")
    for result in results:
        print(f"Result: {result[:100]}...")
        print("-" * 40)