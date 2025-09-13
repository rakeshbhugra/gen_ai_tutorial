import chromadb
import google.generativeai as genai
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()

def create_embeddings(text, model="models/text-embedding-004"):
    """
    Creates embeddings for the input text using Google's Gemini embedding models.
    
    Args:
        text (str): The text to create embeddings for.
        model (str): The embedding model to use. Default is "models/text-embedding-004".
        
    Returns:
        dict: Contains the embedding vector, dimensions, and model used
    """
    # Ensure the API key is set
    if 'GEMINI_API_KEY' not in os.environ:
        raise ValueError("Please set the GEMINI_API_KEY environment variable.")
    
    # Configure Gemini API
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    
    # Create embedding
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_document"  # Optimized for RAG use cases
    )
    
    # Extract the embedding vector
    embedding = response['embedding']
    
    return {
        'text': text,
        'embedding': embedding,
        'dimensions': len(embedding),
        'model': model
    }

def setup_chromadb():
    """Initialize ChromaDB client and collection."""
    client = chromadb.Client(Settings(
        persist_directory="./chroma_db",
        is_persistent=True,
    ))
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}  # Use cosine distance
    )
    
    return client, collection

# initialize ChromaDB client and collection
client, collection = setup_chromadb()

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