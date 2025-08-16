import numpy as np
from .embeddings_example import create_embeddings
from .distance_calculations import cosine_similarity

sentence1 = "How do I get my money back?"

embeddings1 = create_embeddings([sentence1])['embedding'][0]

# print("Sentence Embedding:", embeddings1['embedding'])

sentence2 = "What's your refund policy?"
embeddings2 = create_embeddings([sentence2])['embedding'][0]

sentence3 = "How do I get my money from the bank?"
embeddings3 = create_embeddings([sentence3])['embedding'][0]



similarity = cosine_similarity(embeddings1, embeddings2)
print(f"Cosine similarity between sentence 1 and sentence 2: {similarity}")

similarity = cosine_similarity(embeddings1, embeddings3)
print(f"Cosine similarity between sentence 1 and sentence 3: {similarity}")