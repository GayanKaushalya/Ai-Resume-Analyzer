import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

# Hardcoded technical interview questions dictionary
MOCK_QUESTIONS = {
    "python": [
        "Explain the difference between a list and a tuple in Python.",
        "What are Python generators and decorators, and how do they work?"
    ],
    "fastapi": [
        "What is Dependency Injection in FastAPI, and how do you use 'Depends'?",
        "Explain how FastAPI handles asynchronous code (async/await)."
    ],
    "mongodb": [
        "What is the difference between SQL and NoSQL databases?",
        "How do indexes work in MongoDB, and why are they important?"
    ],
    "docker": [
        "What is the difference between a Docker image and a Docker container?",
        "How does multi-stage building optimize your Dockerfile?"
    ],
    "machine learning": [
        "Explain the difference between supervised and unsupervised learning.",
        "What is overfitting in machine learning, and how can you prevent it?"
    ],
    "git": [
        "What is the difference between 'git merge' and 'git rebase'?",
        "How do you resolve a merge conflict in Git?"
    ]
}

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI-Powered Resume Analyzer & ATS")

# --- SIDEBAR: Authentication ---
st.sidebar.header("User Portal")
auth_mode = st.sidebar.radio("Select Option", ["Login", "Register"])

test_email = st.sidebar.text_input("Email")
test_password = st.sidebar.text_input("Password", type="password")

if auth_mode == "Register":
    if st.sidebar.button("Create Account"):
        res = requests.post(f"{API_URL}/auth/register", json={"email": test_email, "password": test_password})
        if res.status_code == 200:
            st.sidebar.success("Account created successfully! Switch to Login to proceed.")
        else:
            st.sidebar.error(res.json().get("detail", "Registration failed"))

elif auth_mode == "Login":
    if st.sidebar.button("Log In"):
        res = requests.post(f"{API_URL}/auth/login", json={"email": test_email, "password": test_password})
        if res.status_code == 200:
            st.session_state["token"] = res.json().get("access_token")
            st.session_state["user_email"] = test_email
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid credentials.")

# Create Two Tabs
tab1, tab2 = st.tabs(["🔍 Resume Analyzer", "📊 Admin Dashboard"])

# ==========================================
# TAB 1: RESUME ANALYZER & ATS MATCHING
# ==========================================
with tab1:
    if "token" in st.session_state:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        
        # --- RESUME SELECTION (History vs New Upload) ---
        st.subheader("Step 1: Load Resume")
        
        # Fetch previous resumes
        history_res = requests.get(f"{API_URL}/resume/history", headers=headers)
        resume_options = {"--- Upload a New Resume ---": None}
        
        if history_res.status_code == 200:
            for item in history_res.json().get("data", []):
                resume_options[f"Saved: {item['filename']} (Skills: {len(item['skills'])})"] = item['id']
                
        selected_option = st.selectbox("Choose a resume to analyze:", list(resume_options.keys()))
        
        # If user chooses to upload a new one
        if selected_option == "--- Upload a New Resume ---":
            uploaded_file = st.file_uploader("Upload PDF or DOCX file", type=["pdf", "docx", "png", "jpg"])
            if st.button("Upload & Process New Resume") and uploaded_file is not None:
                with st.spinner("Processing document..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    upload_res = requests.post(f"{API_URL}/resume/upload", headers=headers, files=files)
                    
                    if upload_res.status_code == 200:
                        resume_id = upload_res.json().get("resume_id")
                        st.session_state["resume_id"] = resume_id
                        
                        # Immediately analyze skills
                        analyze_res = requests.post(f"{API_URL}/resume/analyze/{resume_id}", headers=headers)
                        if analyze_res.status_code == 200:
                            st.success("New resume processed and analyzed! Check Step 2.")
                            st.rerun() # Refresh to update dropdown lists
                    else:
                        st.error("Upload failed!")
        else:
            # If they chose an existing resume from the dropdown
            st.session_state["resume_id"] = resume_options[selected_option]
            st.info(f"Loaded existing Resume ID: {st.session_state['resume_id']}")

        # --- STEP 2: JOB MATCHING ---
        if "resume_id" in st.session_state and st.session_state["resume_id"] is not None:
            st.markdown("---")
            st.subheader("Step 2: ATS Job Matching")
            job_desc = st.text_area("Paste the Job Description here:")
            
            if st.button("Calculate ATS Score"):
                with st.spinner("Running Machine Learning scoring..."):
                    payload = {"job_description": job_desc}
                    match_res = requests.post(f"{API_URL}/resume/match-job/{st.session_state['resume_id']}", headers=headers, json=payload)
                    
                    if match_res.status_code == 200:
                        data = match_res.json().get("data", {})
                        ats_score = data.get("ats_score")
                        missing_skills = data.get("missing_skills", [])
                        recommendations = data.get("recommendations", [])
                        job_skills = data.get("job_skills_detected", [])
                        
                        st.metric(label="🏆 ATS Compatibility Score", value=f"{ats_score}%")
                        
                        # Columns for results
                        col1, col2 = st.columns(2)
                        with col1:
                            st.warning("⚠️ Missing Skills")
                            for skill in missing_skills:
                                st.write(f"- {skill}")
                        with col2:
                            st.info("💡 AI Recommendations")
                            for rec in recommendations:
                                st.write(f"- {rec}")
                                
                        # --- DOWNLOAD REPORT BUTTON ---
                        report_content = f"=== ATS SCORE REPORT ===\n" \
                                         f"Score: {ats_score}%\n\n" \
                                         f"Required Job Skills: {', '.join(job_skills)}\n" \
                                         f"Missing Skills: {', '.join(missing_skills)}\n\n" \
                                         f"Recommendations:\n" + "\n".join([f"- {r}" for r in recommendations])
                                         
                        st.download_button(
                            label="📥 Download ATS Report", 
                            data=report_content, 
                            file_name="ATS_Report.txt",
                            mime="text/plain"
                        )
                        
                        # --- INTERVIEW QUESTIONS GENERATION ---
                        st.markdown("---")
                        st.subheader("🧑‍💻 AI-Generated Interview Practice Questions")
                        st.caption("Practice these technical questions based on skills found in your resume:")
                        
                        # Find resume document skills to show relevant questions
                        res_doc = requests.get(f"{API_URL}/resume/history", headers=headers)
                        user_skills = []
                        if res_doc.status_code == 200:
                            for r in res_doc.json().get("data", []):
                                if r["id"] == st.session_state["resume_id"]:
                                    user_skills = r["skills"]
                                    
                        found_questions = False
                        for skill in user_skills:
                            if skill in MOCK_QUESTIONS:
                                found_questions = True
                                with st.expander(f"Skill Practice: {skill.upper()}"):
                                    for idx, q in enumerate(MOCK_QUESTIONS[skill]):
                                        st.write(f"**Q{idx+1}:** {q}")
                                        
                        if not found_questions:
                            st.write("No matching technical practice questions found for the skills on this resume yet. Try adding Python or Docker!")
                            
                    else:
                        st.error("Failed to calculate ATS score. Please check that you analyzed the resume first.")
    else:
        st.warning("👈 Please register or log in via the sidebar to access the platform.")

# ==========================================
# TAB 2: ADMIN ANALYTICS DASHBOARD
# ==========================================
with tab2:
    st.subheader("Platform Usage Statistics")
    
    if st.button("Refresh Analytics"):
        res = requests.get(f"{API_URL}/analytics/dashboard")
        
        if res.status_code == 200:
            data = res.json().get("data", {})
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Resumes Uploaded", data.get("total_resumes_uploaded", 0))
            col2.metric("Total Resumes Analyzed", data.get("total_resumes_analyzed", 0))
            col3.metric("Average ATS Score", f"{data.get('average_ats_score', 0)}%")
            
            st.markdown("---")
            
            # Bar Chart
            top_skills = data.get("top_skills", [])
            if top_skills:
                st.write("### 🔥 Most Popular Skills Across All Users")
                df = pd.DataFrame(top_skills)
                df.set_index('skill', inplace=True)
                st.bar_chart(df)
            else:
                st.info("Not enough data to display popular skills yet.")
        else:
            st.error("Failed to load dashboard data.")