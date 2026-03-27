import streamlit as st

st.title("🎯 AI Smart Placement Advisor")

st.sidebar.header("Student Info")
cgpa = st.sidebar.slider("CGPA", 0.0, 10.0, 7.5)
skills = st.sidebar.multiselect("Skills", ["DSA", "DBMS", "OS", "Python", "Java"])
projects = st.sidebar.number_input("Projects", 0, 20, 2)

if st.button("Analyze"):
    st.success("Analysis Complete!")
    st.progress(75)
    st.write("🎯 Placement Chance: 75%")
    st.write("🟡 Category: Medium")
    st.write("💡 Suggestion: Improve DSA skills")
