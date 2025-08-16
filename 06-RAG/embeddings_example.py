import google.generativeai as genai
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

if __name__ == "__main__":
    # Example usage
    text = "The quick brown fox jumps over the lazy dog"
    result = create_embeddings(text)
    
    print(f"Text: '{result['text']}'")
    print(f"Model: {result['model']}")
    print(f"Embedding dimensions: {result['dimensions']}")
    print(f"First 10 dimensions: {result['embedding'][:10]}")
    print(f"Last 10 dimensions: {result['embedding'][-10:]}")