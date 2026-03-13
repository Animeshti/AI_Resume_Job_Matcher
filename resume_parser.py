import pdfminer.high_level
import docx2txt

def extract_text(file_path):

    if file_path.endswith(".pdf"):
        text = pdfminer.high_level.extract_text(file_path)

    elif file_path.endswith(".docx"):
        text = docx2txt.process(file_path)

    else:
        text = ""

    return text.lower() 