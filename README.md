# Resume Screening System
A Python-based automated resume screening system that matches resumes against job descriptions using natural language processing and skill matching algorithms.
## Features
- Processes multiple resume formats (PDF, DOCX, TXT)
- Extracts and normalizes technical skills
- Performs intelligent matching based on:
  - Core technical skills across multiple categories (languages, databases, web, tools, cloud, AI/ML)
  - Experience keywords
  - Required skills from job descriptions
- Calculates match percentages with weighted scoring
- Stores results in SQL Server database
- Supports batch processing of multiple resumes and job descriptions
## System Requirements
- Python 3.x
- SQL Server
- Required Python packages:
  - pyodbc
  - numpy
  - scikit-learn
  - python-docx
  - PyPDF2
## Database Setup
The system requires the following tables in SQL Server:
```sql
CREATE TABLE resumes (
    resume_id INT PRIMARY KEY IDENTITY(1,1),
    file_path VARCHAR(MAX),
    parsed_text TEXT
);
CREATE TABLE job_descriptions (
    job_id INT PRIMARY KEY IDENTITY(1,1),
    job_title VARCHAR(255),
    required_skills VARCHAR(MAX),
    job_description TEXT
);
CREATE TABLE screening_results (
    resume_id INT,
    job_id INT,
    match_percentage FLOAT,
    matching_skills VARCHAR(MAX),
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id),
    FOREIGN KEY (job_id) REFERENCES job_descriptions(job_id)
);
```
## Configuration
1. Update the database connection string in both scripts:
```python
"DRIVER={SQL Server};"
"SERVER=YOUR_SERVER"
"DATABASE=YOUR_DATABASE"
"Trusted_Connection=yes;"
```
2. Set up the file paths for resumes and job descriptions:
```python
resume_files = glob.glob("C:/Users/Asus/Desktop/resumes/*.*")
job_files = os.listdir("C:/Users/Asus/Desktop/job_descriptions")
```
## Usage
1. First, run the job description parser to populate job listings:
```bash
python jobdescriptionparsing.py
```
2. Then, run the resume parser to process resumes and perform matching:
```bash
python resumeparsing.py
```
3. Finally, run the main screening script:
```bash
python main.py
```
## Skill Categories and Weights
The system uses the following categories with corresponding weights:
- Languages (30%): Python, JavaScript, Java, C#, Golang
- Databases (15%): SQL, Oracle, SQL Server
- Web (20%): React, Frontend, Backend, Fullstack
- Tools (10%): MS Office, Excel, PowerPoint, Word
- Cloud (15%): Git, Azure, DevOps, Kubernetes, Linux
- AI/ML (10%): Machine Learning, Deep Learning, TensorFlow, PyTorch, scikit-learn