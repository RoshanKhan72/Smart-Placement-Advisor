import streamlit as st

st.set_page_config(page_title="AI Smart Placement Advisor", page_icon="🎯", layout="wide")

st.title("🎯 AI Smart Placement Advisor")
st.write("Simple test version to check if Streamlit works")

st.sidebar.header("📝 Student Information")
cgpa = st.sidebar.slider("CGPA", min_value=0.0, max_value=10.0, value=7.5)
skills = st.sidebar.multiselect("Skills", ["DSA", "DBMS", "OS", "Python", "Java"])

if st.button("Analyze"):
    st.success(f"CGPA: {cgpa}")
    st.info(f"Skills: {', '.join(skills)}")
    st.balloons()
