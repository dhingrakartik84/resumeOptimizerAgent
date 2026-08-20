import requests
import streamlit as st

st.title("AI Resume Optimizer")

st.caption(
    "Multi-agent resume optimization using "
    "FastAPI, LangGraph, and Ollama"
)

st.header("1. Upload Documents")


left, right = st.columns(2)


with left:
    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"],
        key="resume_file"
    )

with right:
    requirement_file = st.file_uploader(
        "Upload Job Description / Requirement",
        type=["pdf", "docx", "txt"],
        key="requirement_file"
    )

target_role = st.text_input("Target Role",
                            placeholder="Enter the target role for optimization"
)

if st.button("Optimize Resume"):
    if resume_file is None:
        st.error("Please upload a resume.")
    elif requirement_file is None:
        st.error("Please upload a requirement document.")
    else:
        #st.success("Files ready for processing.")
        files = {
            "resume": (
                resume_file.name,
                resume_file.getvalue(),
                resume_file.type
            ),
            "requirement": (
                requirement_file.name,
                requirement_file.getvalue(),
                requirement_file.type
            )
        }

        data = {
            "target_role": target_role,
            "max_revisions": 2
        }
        API_URL = "http://127.0.0.1:8000/api/v1/resumes/optimize"
        response = requests.post(
            API_URL,
            files=files,
            data=data
        )

        if response.ok:
            result = response.json()

            st.success("Resume optimized successfully")

            st.write(result)
        else:
            st.error(
                f"Request failed: {response.status_code}"
            )