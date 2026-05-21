import streamlit as st
import requests

# The URL of your running FastAPI server
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI-Powered Resume Analyzer & ATS")
st.markdown("Upload your resume and see how well it matches your dream job!")

# --- SIDEBAR: Authentication Simulation ---
# For a real app, we'd build a full login form, but for this portfolio UI, 
# we will just use a hardcoded test user to make it easy to demonstrate.
st.sidebar.header("User Settings")
test_email = st.sidebar.text_input("Email", "test@example.com")
test_password = st.sidebar.text_input("Password", "password123", type="password")

if st.sidebar.button("Login to API"):
    # Attempt to login to get the JWT Token
    response = requests.post(f"{API_URL}/auth/login", json={"email": test_email, "password": test_password})
    if response.status_code == 200:
        st.session_state["token"] = response.json().get("access_token")
        st.sidebar.success("Logged in successfully!")
    else:
        st.sidebar.error("Login failed. Did you register this user via the docs?")

# --- MAIN PAGE: Upload & Analyze ---
if "token" in st.session_state:
    st.subheader("Step 1: Upload Resume")
    uploaded_file = st.file_uploader("Upload your PDF or DOCX", type=["pdf", "docx", "png", "jpg"])
    
    if st.button("Upload & Analyze") and uploaded_file is not None:
        with st.spinner("Uploading to AI Engine..."):
            # Prepare the file and headers for the API request
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            # 1. Upload
            upload_res = requests.post(f"{API_URL}/resume/upload", headers=headers, files=files)
            
            if upload_res.status_code == 200:
                resume_id = upload_res.json().get("resume_id")
                st.success(f"Resume uploaded! ID: {resume_id}")
                
                # 2. Analyze
                with st.spinner("Extracting Skills using NLP..."):
                    analyze_res = requests.post(f"{API_URL}/resume/analyze/{resume_id}", headers=headers)
                    if analyze_res.status_code == 200:
                        nlp_data = analyze_res.json().get("data", {})
                        st.write("### 🧠 AI Analysis Results")
                        st.write(f"**Email Found:** {nlp_data.get('email')}")
                        st.write(f"**Skills Detected:** {', '.join(nlp_data.get('skills', []))}")
                        
                        # Save resume_id in session state for Step 2
                        st.session_state["resume_id"] = resume_id
            else:
                st.error(f"Upload failed: {upload_res.text}")
else:
    st.warning("👈 Please login via the sidebar to use the system.")