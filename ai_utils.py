import google.generativeai as genai
from pypdf import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()

def configure_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return None

def analyze_and_generate(resume_text, job_description):
    """
    Analyzes the resume against the JD and generates a tailored cover letter.
    """
    if not configure_genai():
        return "Error: Google API Key Missing in .env file."

    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are an expert data science manager as well as a recruiter. 
    
    RESUME/EXPERIENCE:
    {resume_text}
    
    TARGET JOB DESCRIPTION:
    {job_description}
    
    Please provide a two-part response:
    
    PART 1: RESUME ENHANCEMENTS
    - Identify 3 specific keywords or skills missing from the resume that are emphasized in the JD.
    - Rewrite 2 of the candidate's existing bullet points to better highlight their alignment with the JD using the STAR method.
    
    PART 2: COVER LETTER
    - Write a concise, professional cover letter tailored to this exact role. 
    - Connect the candidate's specific past projects directly to the needs outlined in the JD. 
    - Keep it under 300 words.
    
    Note: The enhancement suggested must be convincing that the user gets shortlisted.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during generation: {e}"
