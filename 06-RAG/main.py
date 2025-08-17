from helper import (
    read_document, 
    chunk_document, 
    create_embeddings_of_chunk,
    add_chunk_to_chromadb
)

def add_document_to_chromadb(document_path, document_name):
    document = read_document(document_path)

    chunks = chunk_document(document)

    for idx, chunk in enumerate(chunks):
        # print(chunk)
        embeddings = create_embeddings_of_chunk(chunk)
        add_chunk_to_chromadb(chunk, embeddings, document_name, idx)
        print(f"Chunk: {chunk[:50]}...\nAdded to ChromaDB with ID: {document_name}_chunk_{idx}\n")
        print("-"*40)

    print("Your document has been successfully processed and added to ChromaDB.")
        

# Worklow:
# Read the document - done
# Chunking the document text - done
# Creating embeddings for the chunk - done
# Adding the emebddings to the chromdb collection - done

if __name__ == "__main__":
    document_path = "data_files/Capabl Customer Support Guide.docx"
    document_name = "Support Guide"

    add_document_to_chromadb(document_path, document_name)
    