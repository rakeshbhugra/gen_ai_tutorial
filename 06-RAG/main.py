from helper import read_document
from chunking_helper import fixed_size_chunking

# Worklow:
# Read the document
# Chunking the document text
def chunk_document(document_text):
    chunks = fixed_size_chunking(
        text=document_text,
        chunk_size=100,
        overlap=10
    )

    return chunks
    


# Creating embeddings for the chunk
# Adding the emebddings to the chromdb collection


if __name__ == "__main__":
    document_path = "data_files/Capabl Customer Support Guide.docx"
    
    document = read_document(document_path)

    chunks = chunk_document(document)

    print(chunks)