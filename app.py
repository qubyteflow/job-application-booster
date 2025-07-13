import os
import streamlit as st
from dotenv import load_dotenv
from google import generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure()
model = genai.GenerativeModel('gemini-1.5-flash')


st.set_page_config(page_title="Job Application Booster", page_icon="💼")

st.title("💼 Job Application Booster")
st.subheader("Step 2: Design Your Application Assistant Interface")


st.header("1. Provide Your Information")


resume = st.text_area("📄 Paste your Resume here", height=250, help="Copy and paste your resume.")
job_desc = st.text_area("📌 Paste the Job Description here", height=250, help="Copy and paste the full job post.")

st.header("2. Choose What to Generate")

col1, col2, col3 = st.columns(3)
with col1:
    generate_cl = st.checkbox("✉️ Cover Letter", value=True)
with col2:
    generate_ri = st.checkbox("📝 Resume Improvements", value=True)
with col3:
    generate_it = st.checkbox("💡 Interview Tips", value=True)

st.header("3. Boost!")

if st.button("🚀 Boost My Application"):
    if not resume or not job_desc:
        st.warning("⚠️ Please fill out both Resume and Job Description.")
    elif not (generate_cl or generate_ri or generate_it):
        st.warning("⚠️ Please select at least one generation option.")
    else:
        with st.spinner("✨ Gemini is generating..."):
            items = []
            if generate_cl:
                items.append("### Cover Letter\nWrite a tailored cover letter to 'Hiring Manager'.")
            if generate_ri:
                items.append("### Resume Improvements\nList 3-5 actionable resume improvements, focusing on keywords and relevance to the job description.")
            if generate_it:
                items.append("### Interview Tips\nList 3-5 concise interview preparation tips specific to this role.")

            full_prompt = f"""
            You are a professional career coach and an expert in job applications.
            Given the following resume and job description, please generate the requested items in clearly separated sections using headings (###).
            Ensure the outputs are professional, concise, and highly relevant
            
            Resume: {resume}
            Job Description: {job_desc}
            Please provide: {" ".join(items)}
            """

            try:
                response = model.generate_content(full_prompt)
                response_text = response.text

                sections = {"Cover Letter": "", "Resume Improvements": "", "Interview Tips": ""}
                current_section = None
    
                for line in response_text.splitlines():
                    if line.startswith("###"):
                        current_section = line.replace("###", "").strip()
                        sections[current_section] = ""
                    elif current_section:
                        sections[current_section] += line + "\n"

                st.markdown("---")
                if generate_cl:
                    st.subheader("✉️ Cover Letter")
                    st.markdown(sections["Cover Letter"])
                    st.code(sections["Cover Letter"], language="text")
    
                if generate_ri:
                    st.subheader("📝 Resume Improvements")
                    st.markdown(sections["Resume Improvements"])
                    st.code(sections["Resume Improvements"], language="text")
    
                if generate_it:
                    st.subheader("💡 Interview Tips")
                    st.markdown(sections["Interview Tips"])
                    st.code(sections["Interview Tips"], language="text")
            except Exception as e:
                st.error(f"Gemini API Error: {e}")


st.markdown("---")
st.caption("Built with ❤️ by QubyteFlow")