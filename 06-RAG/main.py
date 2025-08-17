from helper import read_document, chunk_document
from embeddings_helper import create_embeddings


# Worklow:
# Read the document - done
# Chunking the document text - done
# Creating embeddings for the chunk
# Adding the emebddings to the chromdb collection


def create_embeddings_of_chunk(chunk):
    embeddings = create_embeddings(chunk)
    return embeddings['embedding']
    

if __name__ == "__main__":
    document_path = "data_files/Capabl Customer Support Guide.docx"
    
    document = read_document(document_path)

    chunks = chunk_document(document)

    for chunk in chunks:
        # print(chunk)
        embeddings = create_embeddings_of_chunk(chunk)
        print(f"Chunk: {chunk[:50]}...\nEmbedding: {embeddings[:10]}...")
        print("-"*40)