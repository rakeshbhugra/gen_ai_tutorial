import numpy as np
from .embeddings_example import create_embeddings

def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    Returns value between -1 and 1, where 1 means identical.
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

def euclidean_distance(vec1, vec2):
    """
    Calculate Euclidean distance between two vectors.
    Lower values mean more similar.
    """
    return np.linalg.norm(np.array(vec1) - np.array(vec2))

def vector_arithmetic(word_embeddings, word1, word2, word3):
    """
    Perform vector arithmetic: word1 - word2 + word3
    Example: king - man + woman = queen
    """
    vec1 = np.array(word_embeddings[word1])
    vec2 = np.array(word_embeddings[word2]) 
    vec3 = np.array(word_embeddings[word3])
    
    result_vector = vec1 - vec2 + vec3
    return result_vector

def find_closest_word(target_vector, word_embeddings, exclude_words=None):
    """
    Find the word with embedding closest to target vector.
    """
    if exclude_words is None:
        exclude_words = []
    
    best_similarity = -1
    best_word = None
    
    for word, embedding in word_embeddings.items():
        if word in exclude_words:
            continue
            
        similarity = cosine_similarity(target_vector, embedding)
        if similarity > best_similarity:
            best_similarity = similarity
            best_word = word
    
    return best_word, best_similarity

if __name__ == "__main__":
    print("🔍 EMBEDDING DISTANCE CALCULATIONS")
    print("=" * 50)
    
    # Example 1: Sentence similarity
    print("\n1. SENTENCE SIMILARITY COMPARISON")
    print("-" * 30)
    
    sentences = [
        "I love machine learning",
        "Machine learning is fascinating", 
        "The weather is nice today"
    ]
    
    # Create embeddings for all sentences
    embeddings = {}
    for sentence in sentences:
        result = create_embeddings(sentence)
        embeddings[sentence] = result['embedding']
        print(f"✓ Created embedding for: '{sentence}'")
    
    # Compare similarities
    print(f"\nSimilarity between:")
    s1, s2, s3 = sentences
    
    sim_12 = cosine_similarity(embeddings[s1], embeddings[s2])
    sim_13 = cosine_similarity(embeddings[s1], embeddings[s3])
    
    print(f"'{s1}' vs '{s2}': {sim_12:.4f}")
    print(f"'{s1}' vs '{s3}': {sim_13:.4f}")
    
    if sim_12 > sim_13:
        print(f"✅ As expected: ML sentences are more similar ({sim_12:.4f} > {sim_13:.4f})")
    
    print("\n" + "=" * 50)
    
    # Example 2: Word arithmetic - king - man + woman = queen
    print("\n2. WORD ARITHMETIC: king - man + woman = ?")
    print("-" * 40)
    
    words = ["king", "man", "woman", "queen", "prince", "princess"]
    word_embeddings = {}
    
    print("Creating embeddings for words...")
    for word in words:
        result = create_embeddings(word)
        word_embeddings[word] = result['embedding']
        print(f"✓ {word}")
    
    # Perform vector arithmetic: king - man + woman
    result_vector = vector_arithmetic(word_embeddings, "king", "man", "woman")
    
    # Find closest word (excluding the input words)
    closest_word, similarity = find_closest_word(
        result_vector, 
        word_embeddings, 
        exclude_words=["king", "man", "woman"]
    )
    
    print(f"\nVector arithmetic: king - man + woman")
    print(f"Closest word: '{closest_word}' (similarity: {similarity:.4f})")
    
    if closest_word == "queen":
        print("🎉 Perfect! The arithmetic worked as expected!")
    else:
        print(f"🤔 Got '{closest_word}' instead of 'queen' - embeddings capture some but not all analogies")
    
    print("\n" + "=" * 50)
    print("\n💡 KEY INSIGHTS:")
    print("• Cosine similarity: 1.0 = identical, 0.0 = orthogonal, -1.0 = opposite")
    print("• Similar meanings have higher cosine similarity")
    print("• Vector arithmetic can capture semantic relationships")
    print("• Embeddings encode rich semantic information in high-dimensional space")