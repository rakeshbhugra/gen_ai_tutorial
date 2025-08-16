import chromadb
from chromadb.config import Settings
from .embeddings_example import create_embeddings
from .chunking_example import semantic_chunking
from .distance_calculations import cosine_similarity

def setup_chromadb():
    """Initialize ChromaDB client and collection."""
    client = chromadb.Client(Settings(persist_directory="./chroma_db"))
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}  # Use cosine distance
    )
    
    return client, collection

def add_documents_to_db(collection, documents: list[str]):
    """Chunk documents and add to ChromaDB with embeddings."""
    all_chunks = []
    chunk_ids = []
    
    for doc_id, document in enumerate(documents):
        # Chunk the document
        chunks = semantic_chunking(document, max_chunk_size=200)
        
        for chunk_id, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            chunk_ids.append(f"doc_{doc_id}_chunk_{chunk_id}")
    
    # Create embeddings for all chunks
    embeddings_response = create_embeddings(all_chunks)
    embeddings = [emb for emb in embeddings_response['embedding']]
    
    # Add to ChromaDB
    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=chunk_ids,
        metadatas=[{"doc_id": i//len(chunks)} for i in range(len(all_chunks))]
    )
    
    print(f"Added {len(all_chunks)} chunks to database")

def search_documents(collection, query: str, n_results: int = 3):
    """Search for similar documents using embeddings."""
    # Create embedding for query
    query_embedding = create_embeddings([query])['embedding'][0]
    
    # Search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    return results

if __name__ == "__main__":
    # Sample documents
    documents = [
        """
        Artificial Intelligence is transforming healthcare. AI can analyze medical images, predict diseases, and assist in drug discovery.
        
        Machine learning algorithms help doctors make better diagnoses. They can identify patterns in patient data that humans might miss.
        """,
        """
        Natural language processing is revolutionizing customer service. Chatbots can understand and respond to customer queries 24/7.
        
        Advanced NLP models can handle complex conversations and provide personalized assistance to users.
        """,
        """
        Computer vision technology is advancing rapidly. Self-driving cars use computer vision to navigate roads safely.
        
        Facial recognition systems can identify individuals in security applications. Medical imaging benefits from computer vision for disease detection.
        """
    ]
    
    # Setup ChromaDB
    client, collection = setup_chromadb()
    
    # Add documents
    add_documents_to_db(collection, documents)
    
    # Search examples
    queries = [
        "How does AI help doctors?",
        "What can chatbots do?",
        "How do self-driving cars work?"
    ]
    
    for query in queries:
        print(f"\n=== Query: '{query}' ===")
        results = search_documents(collection, query)
        
        for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0])):
            print(f"Result {i+1} (distance: {distance:.3f}):")
            print(f"  {doc[:100]}...")