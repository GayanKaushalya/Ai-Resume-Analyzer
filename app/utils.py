import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import docx
import os

# IMPORTANT: Tell pytesseract where the Tesseract engine is installed on Windows!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""

def extract_text_from_image(file_path: str) -> str:
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"Error reading Image: {e}")
        return ""

def extract_text(file_path: str, file_ext: str) -> str:
    """Routes the file to the correct extraction function based on its extension."""
    if file_ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        return extract_text_from_docx(file_path)
    elif file_ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(file_path)
    else:
        return ""