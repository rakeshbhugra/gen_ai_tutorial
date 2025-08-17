import docx
from chunking_helper import fixed_size_chunking
from embeddings_helper import create_embeddings
from chromadb_helper import setup_chromadb

# Worklow:
# Read the document - done
# Chunking the document text - done
# Creating embeddings for the chunk - done
# Adding the emebddings to the chromdb collection - done

# Read the document
def read_document(document_path):
    '''
    Reads the full text content from a Microsoft Word (.docx) document.
    
    Parameters:
    document_path (str): The path to the document file.

    Returns:
    str: The full text extracted from the document.

    Notes:
    This function uses the `docx` library to read the document.
    Make sure to install the library using `pip install python-docx` if not already installed

    Usage:
    >>> document_path = "path/to/your/document.docx"
    >>> full_text = read_document(document_path)
    >>> print(full_text)
    '''
    doc = docx.Document(document_path)
    full_text = ""
    for para in doc.paragraphs:
        full_text += para.text + "\n"
    return full_text
    
def chunk_document(document_text):
    chunks = fixed_size_chunking(
        text=document_text,
        chunk_size=100,
        overlap=20
    )

    return chunks

def create_embeddings_of_chunk(chunk):
    embeddings = create_embeddings(chunk)
    return embeddings['embedding']

def add_chunk_to_chromadb(chunk, embeddings, document_name, chunk_index):
    _, collection = setup_chromadb()
    collection.add(
        documents=[chunk],
        embeddings=[embeddings],
        ids=[f"{document_name}_chunk_{chunk_index}"],
        metadatas=[{"doc_name": document_name}]
    )

    return True

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
        
def find_similar_chunks(query):
    # create query embedding
    embeddings = create_embeddings(query)['embedding']

    # Find similar chunks using vector search in our chromadb collection
    _, collection = setup_chromadb()
    results = collection.query(
        query_embeddings=[embeddings],
        n_results=2
    )

    return [x for x in results['documents'][0]]