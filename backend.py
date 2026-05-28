import os
from flask import Flask, request, jsonify, send_from_directory
from PyPDF2 import PdfReader
import io
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smart_placement')
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.get_default_database()
    history_collection = db['analysis_history']
    # Trigger a connection test
    client.admin.command('ping')
    mongo_status = "Connected successfully"
    print("\n" + "="*50)
    print("🚀 SUCCESS: MongoDB Connected Successfully!")
    print("="*50 + "\n", flush=True)
except Exception as e:
    mongo_status = f"Connection failed: {e}"
    print(f"\n❌ ERROR: MongoDB Connection Failed: {e}\n", flush=True)
    db = None
    history_collection = None


# Serve the main HTML page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def calculate_placement_probability(cgpa, num_skills, num_projects, selected_skills):
    cgpa_score = (cgpa / 10.0) * 40
    skills_score = min((num_skills / 5.0) * 30, 30)
    projects_score = min((num_projects / 5.0) * 20, 20)
    
    key_skills = ["DSA", "DBMS", "OS", "Python", "Java"]
    key_skills_count = len([skill for skill in selected_skills if skill in key_skills])
    key_skills_bonus = min((key_skills_count / len(key_skills)) * 10, 10)
    
    total_score = cgpa_score + skills_score + projects_score + key_skills_bonus
    probability = min(total_score, 95)
    
    return probability, {
        'cgpaScore': cgpa_score,
        'skillsScore': skills_score,
        'projectsScore': projects_score,
        'keySkillsBonus': key_skills_bonus
    }

def analyze_skill_gap(selected_skills):
    required_skills = ["DSA", "DBMS", "OS", "OOP"]
    return [skill for skill in required_skills if skill not in selected_skills]

def generate_suggestions(cgpa, num_skills, num_projects, selected_skills, missing_skills):
    suggestions = []
    
    if cgpa < 8.0:
        suggestions.append(f"📚 Improve CGPA above 8.0 → +{int((8.0 - cgpa) * 5)}%")
    
    if num_skills < 4:
        suggestions.append("💡 Learn 2 more skills → +10%")
    
    if num_projects < 3:
        suggestions.append(f"🚀 Add {3 - num_projects} more projects → +{int((3 - num_projects) * 5)}%")
    
    if "DSA" not in selected_skills:
        suggestions.append("🔧 Master Data Structures & Algorithms → +15%")
    
    if missing_skills:
        suggestions.append(f"📖 Focus on missing skills: {', '.join(missing_skills)} → +8%")
    
    return suggestions

def company_prediction(cgpa, num_skills, num_projects, selected_skills):
    predictions = {}
    
    tcs_score = (cgpa / 10.0) * 60 + (num_skills / 10.0) * 20 + (num_projects / 10.0) * 20
    predictions["TCS/Infosys"] = min(tcs_score, 90)
    
    product_score = (cgpa / 10.0) * 30 + (num_skills / 10.0) * 40 + (num_projects / 10.0) * 30
    predictions["Product Companies"] = min(product_score, 85)
    
    startup_score = (cgpa / 10.0) * 35 + (num_skills / 10.0) * 35 + (num_projects / 10.0) * 30
    predictions["Startups"] = min(startup_score, 80)
    
    return predictions

def calculate_resume_score(resume_text):
    if not resume_text:
        return 0
    
    score = 0
    keywords = {
        'Python': 10, 'Java': 10, 'SQL': 8, 'Machine Learning': 15,
        'Projects': 10, 'Experience': 10, 'Skills': 5, 'Leadership': 8,
        'Team': 5, 'Database': 8, 'Algorithm': 10, 'Data Science': 12
    }
    
    resume_lower = resume_text.lower()
    for keyword, points in keywords.items():
        if keyword.lower() in resume_lower:
            score += points
            
    word_count = len(resume_text.split())
    if word_count > 100:
        score += 10
    elif word_count > 50:
        score += 5
        
    return min(score, 100)

def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

@app.route('/api/analyze', methods=['POST'])
def analyze():
    # Form data
    cgpa = float(request.form.get('cgpa', 0))
    num_skills = int(request.form.get('numSkills', 0))
    num_projects = int(request.form.get('numProjects', 0))
    
    # Selected skills usually come as a comma-separated string or multiple fields
    skills_raw = request.form.get('skills', '')
    selected_skills = [s.strip() for s in skills_raw.split(',')] if skills_raw else []

    # Handle PDF file
    resume_text = ""
    if 'resumePdf' in request.files:
        pdf_file = request.files['resumePdf']
        if pdf_file.filename != '':
            resume_text = extract_text_from_pdf(pdf_file)
    
    if not resume_text:
        # Fallback if text was sent directly (for some reason)
        resume_text = request.form.get('resumeText', '')

    probability, score_breakdown = calculate_placement_probability(cgpa, num_skills, num_projects, selected_skills)
    missing_skills = analyze_skill_gap(selected_skills)
    suggestions = generate_suggestions(cgpa, num_skills, num_projects, selected_skills, missing_skills)
    company_predictions = company_prediction(cgpa, num_skills, num_projects, selected_skills)
    resume_score = calculate_resume_score(resume_text)

    results = {
        'probability': probability,
        'scoreBreakdown': score_breakdown,
        'missingSkills': missing_skills,
        'suggestions': suggestions,
        'companyPredictions': company_predictions,
        'resumeScore': resume_score
    }

    # Save to MongoDB
    if history_collection is not None:
        try:
            history_collection.insert_one({
                'timestamp': datetime.utcnow(),
                'inputs': {
                    'cgpa': cgpa,
                    'numSkills': num_skills,
                    'numProjects': num_projects,
                    'selectedSkills': selected_skills
                },
                'results': results
            })
            # Remove the _id from results so it's JSON serializable
            if '_id' in results:
                del results['_id']
        except Exception as e:
            print(f"Error saving to MongoDB: {e}")

    return jsonify(results)

@app.route('/api/db-status', methods=['GET'])
def db_status():
    if db is not None:
        try:
            client.admin.command('ping')
            count = history_collection.count_documents({})
            return jsonify({
                'status': 'success', 
                'message': 'MongoDB Connection Confirmation: Connected successfully!', 
                'uri': MONGO_URI,
                'documents_saved': count
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'MongoDB Connection Confirmation: Failed to ping server. Error: {e}'})
    else:
        return jsonify({'status': 'error', 'message': f'MongoDB Connection Confirmation: Not initialized. {mongo_status}'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
