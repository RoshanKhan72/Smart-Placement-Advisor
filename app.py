import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="AI Smart Placement Advisor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    .high-probability { color: #10b981; font-weight: bold; }
    .medium-probability { color: #f59e0b; font-weight: bold; }
    .low-probability { color: #ef4444; font-weight: bold; }
    .suggestion-box {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🎯 AI Smart Placement Advisor - CI/CD LIVE DEMO</h1>', unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Student Information")
    
    # CGPA Input
    cgpa = st.slider("CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
    
    # Number of Skills
    num_skills = st.number_input("Number of Skills", min_value=0, max_value=10, value=3)
    
    # Number of Projects
    num_projects = st.number_input("Number of Projects", min_value=0, max_value=20, value=2)
    
    # Skills Selection
    st.subheader("Select Your Skills")
    available_skills = ["DSA", "DBMS", "OS", "Python", "Java", "OOP", "Web Development", "Machine Learning"]
    selected_skills = st.multiselect("Choose your skills", available_skills, default=["DSA", "Python"])
    
    # Resume Text Input
    st.subheader("📄 Resume Text")
    resume_text = st.text_area("Paste your resume text here", height=150, 
                               placeholder="Include your skills, projects, experience...")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Analysis Dashboard")
    
    # Analyze Button
    if st.button("🔍 Analyze My Profile", type="primary", use_container_width=True):
        st.session_state.analyzed = True
        
        # Calculate placement probability using rule-based scoring
        def calculate_placement_probability(cgpa, num_skills, num_projects, selected_skills):
            # Base score from CGPA (40% weight)
            cgpa_score = (cgpa / 10.0) * 40
            
            # Skills score (30% weight)
            skills_score = min((num_skills / 5.0) * 30, 30)
            
            # Projects score (20% weight)
            projects_score = min((num_projects / 5.0) * 20, 20)
            
            # Key skills bonus (10% weight)
            key_skills = ["DSA", "DBMS", "OS", "Python", "Java"]
            key_skills_count = len([skill for skill in selected_skills if skill in key_skills])
            key_skills_bonus = min((key_skills_count / len(key_skills)) * 10, 10)
            
            total_score = cgpa_score + skills_score + projects_score + key_skills_bonus
            probability = min(total_score, 95)  # Cap at 95%
            
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
                suggestions.append("💡 Learn 2 more skills → +10%")
            
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
            
            # TCS/Infosys (High weight on CGPA)
            tcs_score = (cgpa / 10.0) * 60 + (num_skills / 10.0) * 20 + (num_projects / 10.0) * 20
            predictions["TCS/Infosys"] = min(tcs_score, 90)
            
            # Product Companies (High weight on skills + projects)
            product_score = (cgpa / 10.0) * 30 + (num_skills / 10.0) * 40 + (num_projects / 10.0) * 30
            predictions["Product Companies"] = min(product_score, 85)
            
            # Startups (Balanced)
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
            
            # Length bonus
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
        
        # Store results in session state
        st.session_state.results = {
            'probability': probability,
            'score_breakdown': score_breakdown,
            'missing_skills': missing_skills,
            'suggestions': suggestions,
            'company_predictions': company_predictions,
            'resume_score': resume_score
        }

# Display results if analyzed
if st.session_state.analyzed and 'results' in st.session_state:
    results = st.session_state.results
    
    # Main Probability Display
    st.subheader("🎯 Overall Placement Probability")
    
    # Determine category
    if results['probability'] >= 70:
        category = "High"
        category_class = "high-probability"
        emoji = "🟢"
    elif results['probability'] >= 40:
        category = "Medium"
        category_class = "medium-probability"
        emoji = "🟡"
    else:
        category = "Low"
        category_class = "low-probability"
        emoji = "🔴"
    
    # Display probability with progress bar
    col_prob1, col_prob2, col_prob3 = st.columns([1, 2, 1])
    with col_prob2:
        st.progress(results['probability'] / 100.0)
        st.markdown(
            f"<h2 style='text-align: center; margin-top: 1rem;'>"
            f"Placement Chance: {results['probability']:.1f}%</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<h3 style='text-align: center;' class='{category_class}'>"
            f"{emoji} Category: {category}</h3>",
            unsafe_allow_html=True,
        )
    
    st.markdown("---")
    
    # Score Breakdown Chart
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📈 Score Breakdown")
        breakdown_data = pd.DataFrame([
            ['CGPA', results['score_breakdown']['cgpa_score']],
            ['Skills', results['score_breakdown']['skills_score']],
            ['Projects', results['score_breakdown']['projects_score']],
            ['Key Skills Bonus', results['score_breakdown']['key_skills_bonus']]
        ], columns=['Component', 'Score'])
        
        st.bar_chart(breakdown_data.set_index('Component'))
    
    with col_chart2:
        st.subheader("🏢 Company-wise Predictions")
        company_data = pd.DataFrame(
            list(results['company_predictions'].items()),
            columns=['Company Type', 'Probability'],
        )
        
        st.bar_chart(company_data.set_index('Company Type'))
    
    st.markdown("---")
    
    # Skill Gap Analysis
    col_gap1, col_gap2 = st.columns(2)
    
    with col_gap1:
        st.subheader("🔍 Skill Gap Analysis")
        if results['missing_skills']:
            st.error(f"Missing Key Skills: {', '.join(results['missing_skills'])}")
        else:
            st.success("✅ You have all the key skills!")
        
        st.write("**Your Current Skills:**")
        for skill in selected_skills:
            st.write(f"• {skill}")
    
    with col_gap2:
        st.subheader("📄 Resume Score")
        st.metric("Resume Score", f"{results['resume_score']}/100")
        
        if results['resume_score'] >= 80:
            st.success("🎉 Excellent resume!")
        elif results['resume_score'] >= 60:
            st.info("👍 Good resume, can be improved")
        else:
            st.warning("⚠️ Resume needs significant improvement")
    
    st.markdown("---")
    
    # Improvement Suggestions
    st.subheader("💡 Improvement Suggestions")
    for suggestion in results['suggestions']:
        st.markdown(f"<div class='suggestion-box'>{suggestion}</div>", unsafe_allow_html=True)

# Instructions section
with col2:
    st.header("📋 How to Use")
    
    st.markdown("""
    ### 🎯 Quick Guide:
    
    1. **Fill Your Details**
       - Adjust CGPA slider
       - Enter skills & projects count
       - Select your technical skills
    
    2. **Paste Resume**
       - Copy-paste your resume text
       - Include keywords for better scoring
    
    3. **Click Analyze**
       - Get instant placement predictions
       - View company-wise chances
       - Receive personalized suggestions
    
    ### 💡 Tips:
    - Be honest with your inputs
    - Include relevant keywords in resume
    - Focus on missing skills for improvement
    """)
    
    st.markdown("---")
    
    st.header("🏆 Success Metrics")
    
    st.markdown("""
    ### 📊 What We Analyze:
    
    **Academic Performance (40%)**
    - CGPA score impact
    
    **Technical Skills (30%)**
    - Number and quality of skills
    
    **Project Experience (20%)**
    - Hands-on project work
    
    **Key Skills Bonus (10%)**
    - Industry-relevant skills
    
    ### 🎯 Categories:
    - **High (70%+)**: Excellent placement chances
    - **Medium (40-70%)**: Good chances with improvements
    - **Low (<40%)**: Need significant improvement
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>🚀 AI Smart Placement Advisor | Hackathon Demo 2024</p>", unsafe_allow_html=True)
