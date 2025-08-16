from dotenv import load_dotenv
import tiktoken

load_dotenv()

def tokenize_text(text):
    """
    Tokenizes the input text and returns both token IDs and decoded tokens.
    
    Args:
        text (str): The text to be tokenized.
        
    Returns:
        dict: Contains token_ids, decoded_tokens, and token_count
    """
    # Use tiktoken for actual tokenization (compatible with OpenAI models)
    # This is essential for RAG systems because:
    # 1. We need to understand how text is chunked by the model
    # 2. Token limits are crucial for API calls and embeddings
    # 3. Different tokens can have different semantic meanings
    # 4. Helps optimize text splitting for better retrieval
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
    
    # Encode text to token IDs
    token_ids = encoding.encode(text)
    
    # Decode each token ID back to see the actual text pieces
    # This shows us exactly how the model "sees" and processes the text
    decoded_tokens = [encoding.decode([token_id]) for token_id in token_ids]
    
    return {
        'token_ids': token_ids,
        'decoded_tokens': decoded_tokens,
        'token_count': len(token_ids)
    }

if __name__ == "__main__":
    # Example usage with different types of text to show tokenization patterns
    text = "Hello, how are you?"
    result = tokenize_text(text)
    
    print(f"Original text: '{text}'")
    print(f"Token count: {result['token_count']}")
    print(f"Token IDs: {result['token_ids']}")
    print(f"Decoded tokens: {result['decoded_tokens']}")
    print()
    
    # Show how tokenization works with more complex text
    complex_text = "The quick brown fox jumps over the lazy dog. This sentence contains 123 numbers and special@characters!"
    complex_result = tokenize_text(complex_text)
    
    print(f"Complex text: '{complex_text}'")
    print(f"Token count: {complex_result['token_count']}")
    print("Token breakdown:")
    for i, (token_id, decoded) in enumerate(zip(complex_result['token_ids'], complex_result['decoded_tokens'])):
        print(f"  {i+1:2d}: ID={token_id:5d} -> '{decoded}'")