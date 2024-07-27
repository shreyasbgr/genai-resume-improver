import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-pro-001')
    response = model.generate_content(input)
    return response.text

def input_pdf_setup(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    pdf_content = ""
    for page in reader.pages:
        pdf_content+=str(page.extract_text())
    return pdf_content

input_prompt = """
Hey act like a skilled or very experienced ATS(Applicant Tracking System) with a deep
understanding of the role given in the job description. Your task is to evaluate the resume against the provided job description.
You must consider the job market is very competitive and you should provide the best assistance for improving the reusme.
Assign the percentage matching based on the job description, the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in one single string having the structure with below sections:
JDmatch (Percentage match), Missing keywords, Profile summary.
"""

# Streamlit app
st.title("ATS Resume Improver")
st.text("Improve your resume ATS")
jd = st.text_area("Job Description")
uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=pdf_content, jd=jd))
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")