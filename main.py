import pyodbc
import re

def connect_to_db():
    """Establish database connection"""
    connection = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=YOUR_SERVER"
        "DATABASE=YOUR_DATABASE"
        "Trusted_Connection=yes;"
    )
    return connection

def preprocess_technical_text(text):
    """Enhanced preprocessing for technical text"""
    text = text.lower()
    replacements = {
        'javascript': 'js',
        'react.js': 'react',
        'reactjs': 'react',
        'node.js': 'nodejs',
        'microsoft azure': 'azure',
        'ms azure': 'azure',
        'git hub': 'github',
        'microsoft office': 'ms office',
        'sql server': 'sqlserver',
        'machine learning': 'ml',
        'deep learning': 'dl',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    text = re.sub(r'([\/\-\+\#])', r' \1 ', text)
    return text.strip()

def calculate_enhanced_similarity_improved(resume_text, job_text):
    """Enhanced version to match all relevant skills and calculate match percentage."""
    processed_resume = preprocess_technical_text(resume_text)
    processed_job = preprocess_technical_text(job_text)
    
    core_skills = {
        'languages': {
            'python': r'\b(python)\b',
            'javascript': r'\b(javascript|js)\b',
            'java': r'\b(java)\b(?!\s*script)',
            'c#': r'\b(c#|csharp)\b',
            'golang': r'\b(golang|go)\b'
        },
        'databases': {
            'sql': r'\b(sql|mysql)\b',
            'oracle': r'\b(oracle)\b',
            'sqlserver': r'\b(sql\s*server|sqlserver)\b'
        },
        'web': {
            'react': r'\b(react|react\.js|reactjs)\b',
            'frontend': r'\b(frontend|front-end)\b',
            'backend': r'\b(backend|back-end)\b',
            'fullstack': r'\b(fullstack|full-stack)\b'
        },
        'tools': {
            'ms office': r'\b(ms\s*office|microsoft\s*office)\b',
            'excel': r'\b(excel)\b',
            'powerpoint': r'\b(powerpoint)\b',
            'word': r'\b(word)\b'
        },
        'cloud': {
            'git': r'\b(git)\b(?!\w)',
            'azure': r'\b(azure)\b',
            'devops': r'\b(devops)\b',
            'kubernetes': r'\b(kubernetes|k8s)\b',
            'linux': r'\b(linux)\b'
        },
        'ai_ml': {
            'machine learning': r'\b(machine\s*learning)\b',
            'deep learning': r'\b(deep\s*learning)\b',
            'tensorflow': r'\b(tensorflow)\b',
            'pytorch': r'\b(pytorch)\b',
            'sklearn': r'\b(sklearn|scikit-learn)\b'
        }
    }
    
    scores = {}
    matched_skills = set()
    
    for category, skills in core_skills.items():
        required_skills = {skill for skill, pattern in skills.items()
                           if re.search(pattern, processed_job, re.IGNORECASE)}
        matches = 0
        
        for skill, pattern in skills.items():
            if skill in required_skills and re.search(pattern, processed_resume, re.IGNORECASE):
                matches += 1
                matched_skills.add(skill)
        
        if required_skills:
            scores[category] = matches / len(required_skills)
    
    category_weights = {
        'languages': 0.30,
        'databases': 0.15,
        'web': 0.20,
        'tools': 0.10,
        'cloud': 0.15,
        'ai_ml': 0.10
    }
    
    final_score = sum(scores.get(category, 0) * category_weights.get(category, 0.1)
                      for category in core_skills)
    
    experience_keywords = {'software engineer', 'developer', 'web development', 'full stack'}
    experience_matches = sum(1 for keyword in experience_keywords
                              if re.search(r'\b' + re.escape(keyword) + r'\b',
                                           processed_resume, re.IGNORECASE))
    experience_bonus = min(0.2, experience_matches * 0.05)
    
    final_score = min(100, (final_score + experience_bonus) * 100)
    
    return final_score, list(matched_skills)

def main():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM screening_results")
        connection.commit()

        cursor.execute("SELECT resume_id, file_path, parsed_text FROM resumes")
        resumes = cursor.fetchall()
        
        cursor.execute("SELECT job_id, job_title, job_description FROM job_descriptions")
        job_descriptions = cursor.fetchall()

        results = []
        for resume in resumes:
            resume_id, file_path, resume_text = resume
            
            for job in job_descriptions:
                job_id, job_title, job_text = job
                
                match_score, matching_skills = calculate_enhanced_similarity_improved(resume_text, job_text)
                
                cursor.execute("""
                    INSERT INTO screening_results (resume_id, job_id, match_percentage, matching_skills) 
                    VALUES (?, ?, ?, ?)
                """, resume_id, job_id, match_score, ', '.join(matching_skills))
                
                results.append({
                    'file_path': file_path,
                    'job_title': job_title,
                    'match_percentage': match_score,
                    'matching_skills': matching_skills
                })
                
                connection.commit()

        results.sort(key=lambda x: x['match_percentage'], reverse=True)
        print("\nMatching Results:")
        print("=" * 80)
        for result in results:
            print(f"Resume: {result['file_path']}")
            print(f"Job: {result['job_title']}")
            print(f"Match Percentage: {result['match_percentage']:.2f}%")
            print(f"Matching Skills: {', '.join(result['matching_skills'])}")
            print("-" * 80)

    except Exception as e:
        print(f"Error in main execution: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    main()