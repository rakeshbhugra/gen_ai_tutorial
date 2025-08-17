from chromadb_helper import setup_chromadb, add_document_to_db
from docx import Document
from chunking_helper import fixed_size_chunking
from embeddings_helper import create_embeddings
import os

document_path = "data_files/Capabl Customer Support Guide.docx"
document_name = "Capable Customer Support Guide"

# Ensure the document exists
if not os.path.exists(document_path):
    raise FileNotFoundError(f"The document {document_path} does not exist.")

# Initialize ChromaDB client and collection
client, collection = setup_chromadb()

# Initialize the document
doc = Document(document_path)

# Extract full text from the document
full_text = ""
for para in doc.paragraphs:
    full_text += para.text + "\n"

# Chunk the document text
chunks = fixed_size_chunking(full_text, chunk_size=100, overlap=10)

# Add each chunk to the ChromaDB collection
for i, chunk in enumerate(chunks):
    # Create embeddings for the chunk
    embeddings = create_embeddings(chunk)
    # Add the document to the database
    collection.add(
        documents=[chunk],
        embeddings=[embeddings['embedding']],
        ids=[f"{document_name}_chunk_{i}"],
        metadatas=[{"doc_name":f"{document_name}"}]
    )
    print(f"Added chunk_{i} to the collection.")

print(f"Total {len(chunks)} chunks added to the collection.")