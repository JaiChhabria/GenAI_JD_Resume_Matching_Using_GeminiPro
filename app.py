import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() #load all the dependencies in the environment

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Gemini Pro Response

def get_gemini_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text



## Get text from PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text)
    return text



#Prompt Template

input_prompt = """
Hey act like a skilled or very experienced ATS(Application Tracking System) with a deep understanding of tech field, software engineering, data science, data analyst, and
big data engineer. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide best assistance
for improving the resume. Assign the percentage Matching based on JD and the missing keywords with high accuracy
resume:{text}
description: {jd}

I want the response in one single string having the structure
{{"JD Match": "%","MissingKeywords:[]","Profile Summary":""}}
"""


## Streamlit App

st.title("JD To Resume Match")
st.text("Improve Your Resume Match")
js=st.text_area("Paste your Job Description")
uploaded_file=st.file_uploader("Upload Your Resume", type='pdf',help="Please upload your resume in the PDF format")

submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)
        



        

