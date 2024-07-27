import base64
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image

import google.generativeai as genai
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-001')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def pdf_input_setup(uploaded_file):
    """
    Converts a multi-page PDF file uploaded by the user into a list of image parts.

    Parameters:
        uploaded_file (file-like object): The uploaded PDF file.

    Returns:
        list: A list of dictionaries representing the image parts. Each dictionary contains the following keys:
            - mime_type (str): The MIME type of the image part.
            - data (str): The base64-encoded data of the image part.

    Raises:
        FileNotFoundError: If no file is uploaded.
    """
    if uploaded_file is not None:
        # Convert the PDF to images (one image per page)
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        pdf_parts = []
        for image in images:
            # Convert each image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            # Append the image part to the list
            pdf_parts.append(
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()  # encode to base 64
                }
            )

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Streamlit app setup
st.set_page_config(page_title="GenAI ATS Resume Improver", layout="wide")
st.header("GenAI ATS Resume Improver")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf")

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about my resume")
submit2 = st.button("Percentage match")

input_prompt1 = """
You are an experienced Human Resource Hiring Manager in the role specified in the job description. Your task is to review the provided resume
against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job description.
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of the role specified in the job description. You have the ability to scan resumes for relevant keywords and have a deep ATS functionality understanding.
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches the job description. First the output should come as a percentage and then keywords missing and then last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = pdf_input_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

if submit2:
    if uploaded_file is not None:
        pdf_content = pdf_input_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")