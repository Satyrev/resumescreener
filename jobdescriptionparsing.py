import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from docx import Document
from PyPDF2 import PdfReader
import pyodbc 
from sklearn.feature_extraction.text import TfidfVectorizer

SKILL_KEYWORDS = [
    "python", "java", "sql", "tensorflow", "machine learning", "data analysis",
    "project management", "git", "linux", "scripting", "cloud", "kubernetes",
    "golang", "pytorch", "sklearn", "azure", "aws", "gcp", "mlops", "neural networks",
    "transformers", "generative ai", "llms"
]

def extract_required_skills(text):
    vectorizer = TfidfVectorizer(vocabulary=[kw.lower() for kw in SKILL_KEYWORDS])
    matrix = vectorizer.fit_transform([text.lower()])
    matched_skills = vectorizer.get_feature_names_out()[matrix.toarray().any(axis=0)]
    return ", ".join(matched_skills)


def parse_word(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def parse_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def parse_job_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == ".pdf":
        return parse_pdf(file_path)
    elif ext.lower() == ".docx":
        return parse_word(file_path)
    elif ext.lower() == ".txt":
        return parse_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

import re

import re

import re

def extract_job_title(text):
    title_patterns = [
        r"(?i)\b(job title|position|co-op student position title):?\s*(.+)",
        r"(?i)\btitle:?\s*(.+)",
        r"(?i)\bco-op student position title:?\s*(.+)",
    ]
    for pattern in title_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(2).split("\n")[0].strip()

    for line in text.split("\n"):
        if len(line.strip()) > 5:
            return line.strip()
    return "Unknown Title"



def extract_required_skills(text):
    skills = [skill for skill in SKILL_KEYWORDS if skill.lower() in text.lower()]
    return ", ".join(skills)

def parse_job_description(text):
    patterns_to_remove = [
        r"(?i)(job title|position|requirements|skills required|about us):.*",
        r"(?i)(additional information|disclaimer).*",
        r"(?i)(nokia offers|what we offer).*",
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.DOTALL)

    return text.strip()


connection = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=YOUR_SERVER"
    "DATABASE=YOUR_DATABASE"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()

job_files = os.listdir("C:/Users/Asus/Desktop/job_descriptions")

for file_name in job_files:
    file_path = os.path.join("C:/Users/Asus/Desktop/job_descriptions", file_name)
    try:
        text = parse_job_file(file_path)

        job_title = extract_job_title(text)
        required_skills = extract_required_skills(text)
        job_description = parse_job_description(text)
        

        cursor.execute("""
            INSERT INTO job_descriptions (job_title, required_skills, job_description)
            VALUES (?, ?, ?)
        """, job_title, required_skills, job_description)
        connection.commit()
        print(f"Processed and inserted: {file_name}")
    except Exception as e:
        print(f"Failed to process {file_name}: {e}")

connection.close()
