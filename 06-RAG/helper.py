import docx

print("you are importing the helper.py file")

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
    