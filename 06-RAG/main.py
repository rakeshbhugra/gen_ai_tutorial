from helper import read_document, chunk_document


# Worklow:
# Read the document
# Chunking the document text
# Creating embeddings for the chunk
# Adding the emebddings to the chromdb collection


if __name__ == "__main__":
    document_path = "data_files/Capabl Customer Support Guide.docx"
    
    document = read_document(document_path)

    chunks = chunk_document(document)

    for chunk in chunks:
        print(chunk)
        print("-"*40)