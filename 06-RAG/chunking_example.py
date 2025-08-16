import re
from typing import List

def simple_sentence_chunking(text: str) -> List[str]:
    """Split text into sentences using basic punctuation."""
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def fixed_size_chunking(text: str, chunk_size: int = 100, overlap: int = 20) -> List[str]:
    """Split text into fixed-size chunks with overlap."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks

def semantic_chunking(text: str, max_chunk_size: int = 200) -> List[str]:
    """Split text at paragraph boundaries, respecting max size."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= max_chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

# Example text
sample_text = """
Artificial Intelligence is transforming the world. It has applications in healthcare, finance, and transportation.

Machine learning is a subset of AI. It enables computers to learn from data without explicit programming. Deep learning uses neural networks with multiple layers.

Natural language processing helps computers understand human language. It powers chatbots, translation services, and search engines.

Computer vision allows machines to interpret visual information. It's used in autonomous vehicles, medical imaging, and security systems.
"""

if __name__ == "__main__":
    print("=== Sentence Chunking ===")
    sentence_chunks = simple_sentence_chunking(sample_text)
    for i, chunk in enumerate(sentence_chunks):
        print(f"Chunk {i+1}: {chunk}")
    
    print("\n=== Fixed Size Chunking ===")
    fixed_chunks = fixed_size_chunking(sample_text, chunk_size=50, overlap=10)
    for i, chunk in enumerate(fixed_chunks):
        print(f"Chunk {i+1}: {chunk}")
    
    print("\n=== Semantic Chunking ===")
    semantic_chunks = semantic_chunking(sample_text, max_chunk_size=150)
    for i, chunk in enumerate(semantic_chunks):
        print(f"Chunk {i+1}: {chunk}")