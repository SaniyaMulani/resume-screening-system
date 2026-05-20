# utils.py

import re
import PyPDF2


# Extract Text From PDF
def extract_text(file):

    text = ""

    pdf = PyPDF2.PdfReader(file)

    for page in pdf.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted

    return text


# Clean Text
def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    return text


# Extract Email
def extract_email(text):

    match = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",
        text
    )

    return match[0] if match else "Not Found"


# Extract Phone Number
def extract_phone(text):

    match = re.findall(r'\b\d{10}\b', text)

    return match[0] if match else "Not Found"