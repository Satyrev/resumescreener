from PyPDF2 import PdfReader
from docx import Document
import os
import pyodbc
import glob
import re

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def parse_word(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def parse_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def parse_resume(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    if ext == '.pdf':
        return parse_pdf(file_path)
    elif ext in ['.docx']:
        return parse_word(file_path)
    elif ext in ['.txt']:
        return parse_text(file_path)
    else:
        raise ValueError("Unsupported file type")
    


def preprocess_text(text):
    
    text = re.sub(r"[^a-zA-Z0-9@/#\+.\s]", "", text)
    
    text = text.lower()
    
    keywords = text.split()
    return " ".join(keywords)




connection = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=YOUR_SERVER"
    "DATABASE=YOUR_DATABASE"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()


cursor.execute("SELECT ISNULL(MAX(resume_id), 0) FROM resumes")
max_resume_id = cursor.fetchone()[0]

resume_id = max_resume_id + 1  

default_job_id = 1  

resume_files = glob.glob("C:/Users/Asus/Desktop/resumes/*.*")

for file_path in resume_files:
    try:
        parsed_text = preprocess_text(parse_resume(file_path))
        cursor.execute("""
            INSERT INTO resumes (file_path, parsed_text)
            VALUES (?, ?)
            """, file_path, parsed_text)

        connection.commit()

        print(f"Inserted: {file_path}")
        resume_id += 1  
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")



