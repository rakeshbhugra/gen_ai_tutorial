from helper import read_document, chunk_document, create_embeddings_of_chunk
from chromadb_helper import setup_chromadb

# Worklow:
# Read the document - done
# Chunking the document text - done
# Creating embeddings for the chunk - done
# Adding the emebddings to the chromdb collection


def add_chunk_to_chromadb(chunk, embeddings, document_name, chunk_index):
    _, collection = setup_chromadb()
    collection.add(
        documents=[chunk],
        embeddings=[embeddings],
        ids=[f"{document_name}_chunk_{chunk_index}"],
        metadatas=[{"doc_name": document_name}]
    )

    return True

    
if __name__ == "__main__":
    document_path = "data_files/Capabl Customer Support Guide.docx"
    document_name = "Support Guide"
    
    document = read_document(document_path)

    chunks = chunk_document(document)

    for idx, chunk in enumerate(chunks):
        # print(chunk)
        embeddings = create_embeddings_of_chunk(chunk)
        add_chunk_to_chromadb(chunk, embeddings, document_name, idx)
        print(f"Chunk: {chunk[:50]}...\nAdded to ChromaDB with ID: {document_name}_chunk_{idx}\n")
        print("-"*40)