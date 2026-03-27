import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="AI Smart Placement Advisor",
    page_icon="🎯",
    layout="wide"
)

# Title
st.title("🎯 AI Smart Placement Advisor")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("📝 Student Information")

# CGPA Input
cgpa = st.sidebar.slider("CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.1)

# Number of Skills
num_skills = st.sidebar.number_input("Number of Skills", min_value=0, max_value=10, value=3)

# Number of Projects
num_projects = st.sidebar.number_input("Number of Projects", min_value=0, max_value=20, value=2)

# Skills Selection
st.sidebar.subheader("Select Your Skills")
available_skills = ["DSA", "DBMS", "OS", "Python", "Java", "OOP", "Web Development", "Machine Learning"]
selected_skills = st.sidebar.multiselect("Choose your skills", available_skills, default=["DSA", "Python"])

# Resume Text Input
st.sidebar.subheader("📄 Resume Text")
resume_text = st.sidebar.text_area("Paste your resume text here", height=150, 
                                   placeholder="Include your skills, projects, experience...")

# Main content
st.header("📊 Analysis Dashboard")

# Analyze Button
if st.button("🔍 Analyze My Profile", type="primary"):
    
    # Calculate placement probability
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
            'cgpa_score': cgpa_score,
            'skills_score': skills_score,
            'projects_score': projects_score,
            'key_skills_bonus': key_skills_bonus
        }
    
    # Skill Gap Analyzer
    def analyze_skill_gap(selected_skills):
        required_skills = ["DSA", "DBMS", "OS", "OOP"]
        missing_skills = [skill for skill in required_skills if skill not in selected_skills]
        return missing_skills
    
    # Improvement Suggestions
    def generate_suggestions(cgpa, num_skills, num_projects, selected_skills, missing_skills):
        suggestions = []
        
        if cgpa < 8.0:
            suggestions.append(f"📚 Improve CGPA above 8.0 → +{int((8.0 - cgpa) * 5)}%")
        
        if num_skills < 4:
            suggestions.append(f"💡 Learn 2 more skills → +10%")
        
        if num_projects < 3:
            suggestions.append(f"🚀 Add {3 - num_projects} more projects → +{int((3 - num_projects) * 5)}%")
        
        if "DSA" not in selected_skills:
            suggestions.append("🔧 Master Data Structures & Algorithms → +15%")
        
        if missing_skills:
            suggestions.append(f"📖 Focus on missing skills: {', '.join(missing_skills)} → +8%")
        
        return suggestions
    
    # Company-wise Prediction
    def company_prediction(cgpa, num_skills, num_projects, selected_skills):
        predictions = {}
        
        tcs_score = (cgpa / 10.0) * 60 + (num_skills / 10.0) * 20 + (num_projects / 10.0) * 20
        predictions["TCS/Infosys"] = min(tcs_score, 90)
        
        product_score = (cgpa / 10.0) * 30 + (num_skills / 10.0) * 40 + (num_projects / 10.0) * 30
        predictions["Product Companies"] = min(product_score, 85)
        
        startup_score = (cgpa / 10.0) * 35 + (num_skills / 10.0) * 35 + (num_projects / 10.0) * 30
        predictions["Startups"] = min(startup_score, 80)
        
        return predictions
    
    # Resume Score
    def calculate_resume_score(resume_text):
        if not resume_text:
            return 0
        
        score = 0
        keywords = {
            'Python': 10, 'Java': 10, 'SQL': 8, 'Machine Learning': 15,
            'Projects': 10, 'Experience': 10, 'Skills': 5, 'Leadership': 8,
            'Team': 5, 'Database': 8, 'Algorithm': 10, 'Data Science': 12
        }
        
        for keyword, points in keywords.items():
            if keyword.lower() in resume_text.lower():
                score += points
        
        if len(resume_text.split()) > 100:
            score += 10
        elif len(resume_text.split()) > 50:
            score += 5
        
        return min(score, 100)
    
    # Perform calculations
    probability, score_breakdown = calculate_placement_probability(cgpa, num_skills, num_projects, selected_skills)
    missing_skills = analyze_skill_gap(selected_skills)
    suggestions = generate_suggestions(cgpa, num_skills, num_projects, selected_skills, missing_skills)
    company_predictions = company_prediction(cgpa, num_skills, num_projects, selected_skills)
    resume_score = calculate_resume_score(resume_text)
    
    # Display results
    st.success("🎉 Analysis Complete!")
    
    # Main Probability Display
    st.subheader("🎯 Overall Placement Probability")
    
    # Determine category
    if probability >= 70:
        category = "High"
        emoji = "🟢"
    elif probability >= 40:
        category = "Medium"
        emoji = "🟡"
    else:
        category = "Low"
        emoji = "🔴"
    
    # Display probability
    st.progress(probability / 100.0)
    st.markdown(f"## Placement Chance: {probability:.1f}%")
    st.markdown(f"### {emoji} Category: {category}")
    
    st.markdown("---")
    
    # Score Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Score Breakdown")
        st.write(f"**CGPA Score:** {score_breakdown['cgpa_score']:.1f}/40")
        st.write(f"**Skills Score:** {score_breakdown['skills_score']:.1f}/30")
        st.write(f"**Projects Score:** {score_breakdown['projects_score']:.1f}/20")
        st.write(f"**Key Skills Bonus:** {score_breakdown['key_skills_bonus']:.1f}/10")
    
    with col2:
        st.subheader("🏢 Company-wise Predictions")
        for company, prob in company_predictions.items():
            st.write(f"**{company}:** {prob:.1f}%")
    
    st.markdown("---")
    
    # Skill Gap Analysis
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("🔍 Skill Gap Analysis")
        if missing_skills:
            st.error(f"Missing Key Skills: {', '.join(missing_skills)}")
        else:
            st.success("✅ You have all the key skills!")
        
        st.write("**Your Current Skills:**")
        for skill in selected_skills:
            st.write(f"• {skill}")
    
    with col4:
        st.subheader("📄 Resume Score")
        st.metric("Resume Score", f"{resume_score}/100")
        
        if resume_score >= 80:
            st.success("🎉 Excellent resume!")
        elif resume_score >= 60:
            st.info("👍 Good resume, can be improved")
        else:
            st.warning("⚠️ Resume needs significant improvement")
    
    st.markdown("---")
    
    # Improvement Suggestions
    st.subheader("💡 Improvement Suggestions")
    for suggestion in suggestions:
        st.info(suggestion)

# Instructions
st.markdown("---")
st.header("📋 How to Use")
st.markdown("""
1. **Fill Your Details** (Sidebar)
   - Adjust CGPA slider
   - Enter skills & projects count
   - Select your technical skills
   - Paste your resume text

2. **Click Analyze**
   - Get instant placement predictions
   - View company-wise chances
   - Receive personalized suggestions

3. **Review Results**
   - Check your placement probability
   - Identify skill gaps
   - Follow improvement suggestions
""")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🚀 AI Smart Placement Advisor | Hackathon Demo 2024</p>", unsafe_allow_html=True)
