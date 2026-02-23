import streamlit as st
import os
from dotenv import load_dotenv
import ai_utils 

load_dotenv()

st.set_page_config(page_title="AI Career Assistant", page_icon="📄", layout="wide")

st.title("📄 AI Resume Enhancer & Cover Letter Generator")
st.write("Upload your resume (or edit the text directly) and paste a target Job Description to get tailored enhancements and a draft cover letter.")

if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ Google API Key missing from .env file!")

# Default texts for easy testing and portfolio demonstration
default_resume = """Data Scientist
Skills: Python, Machine Learning, Generative AI, PySpark, Pandas.
Key Projects:
- <Project 1>: Description 1
- <Project 2>: Description 2
- <Project 3>: Description 3
- <Project 4>: Description 4"""

default_jd = """Senior Data Scientist (Based in Southeast Asia or Japan)
Requirements:
- Strong proficiency in Python and ML frameworks.
- Experience building and deploying Generative AI applications.
- Proven track record of delivering high-impact optimization and forecasting models in a retail or enterprise environment.
- Ability to communicate complex data concepts to stakeholders."""

# Sidebar for PDF Upload
with st.sidebar:
    st.header("Upload Resume")
    uploaded_file = st.file_uploader("📄 Upload PDF Resume (Optional)", type="pdf")
    if uploaded_file:
        with st.spinner("Extracting text..."):
            extracted_text = ai_utils.extract_text_from_pdf(uploaded_file)
            if extracted_text:
                st.session_state['resume_text'] = extracted_text
                st.success("Text extracted successfully!")
            else:
                st.error("Failed to extract text from PDF.")

# Main Layout: Two Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Experience")
    # If a PDF was uploaded, use that text. Otherwise, use the default.
    current_resume = st.session_state.get('resume_text', default_resume)
    resume_input = st.text_area("Edit your resume text here:", value=current_resume, height=350)

with col2:
    st.subheader("Target Job Description")
    jd_input = st.text_area("Paste the JD here:", value=default_jd, height=350)

st.markdown("---")

# Generation Trigger
if st.button("✨ Analyze & Generate", type="primary"):
    if not resume_input.strip() or not jd_input.strip():
        st.warning("Please provide both resume details and a job description.")
    else:
        with st.spinner("Analyzing alignment and drafting documents..."):
            result = ai_utils.analyze_and_generate(resume_input, jd_input)
            st.success("Generation Complete!")
            
            st.markdown("### Your Results")
            st.write(result)
