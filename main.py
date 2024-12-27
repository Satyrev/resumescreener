import pyodbc


connection = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=YOUR_SERVER" 
    "DATABASE=YOUR_DATABASE"  
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()


cursor.execute("SELECT job_id, job_title, required_skills, job_description FROM job_description")
job_descriptions = cursor.fetchall()
print(job_descriptions)


cursor.execute("SELECT resume_id, file_path, parsed_text FROM resumes")
resumes = cursor.fetchall()
print(resumes)

def match_skills(resume_text, required_skills):
    resume_skills = set(resume_text.lower().split(", "))
    job_skills = set(required_skills.lower().split(", "))
    matches = resume_skills.intersection(job_skills)
    return matches, len(matches) / len(job_skills)

for resume in resumes:
    for job in job_descriptions:
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM screening_results 
            WHERE resume_id = ? AND job_id = ?
        """, resume[0], job[0])
        count = cursor.fetchone()[0]
        
        if count == 0:  
            matches, percentage = match_skills(resume[2], job[2])
            matching_skills = ", ".join(matches)

            cursor.execute("""
                INSERT INTO screening_results (resume_id, job_id, match_percentage, matching_skills) 
                VALUES (?, ?, ?, ?)
            """, resume[0], job[0], percentage, matching_skills)
            connection.commit()

cursor.execute("""
    SELECT DISTINCT r.file_path, j.job_title, s.match_percentage, s.matching_skills
    FROM screening_results s
    JOIN resumes r ON s.resume_id = r.resume_id
    JOIN job_description j ON s.job_id = j.job_id
""")

for row in cursor.fetchall():
    print(f"Resume: {row.file_path}, Job: {row.job_title}, Match: {row.match_percentage:.2%}, Skills: {row.matching_skills}")
