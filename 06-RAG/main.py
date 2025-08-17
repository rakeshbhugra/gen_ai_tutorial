from helper import add_document_to_chromadb

if __name__ == "__main__":
    document_path = "data_files/Capabl Customer Support Guide.docx"
    document_name = "Support Guide"

    add_document_to_chromadb(document_path, document_name)
    