import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI-Powered Resume Analyzer & ATS")

# --- SIDEBAR: Authentication ---
st.sidebar.header("User Settings")
test_email = st.sidebar.text_input("Email", "test@example.com")
test_password = st.sidebar.text_input("Password", "password123", type="password")

if st.sidebar.button("Login to API"):
    response = requests.post(f"{API_URL}/auth/login", json={"email": test_email, "password": test_password})
    if response.status_code == 200:
        st.session_state["token"] = response.json().get("access_token")
        st.sidebar.success("Logged in successfully!")
    else:
        st.sidebar.error("Login failed.")

# Create Two Tabs!
tab1, tab2 = st.tabs(["🔍 Resume Analyzer", "📊 Admin Dashboard"])

# ==========================================
# TAB 1: RESUME ANALYZER & ATS MATCHING
# ==========================================
with tab1:
    if "token" in st.session_state:
        st.subheader("Step 1: Upload Resume")
        uploaded_file = st.file_uploader("Upload your PDF or DOCX", type=["pdf", "docx", "png", "jpg"])
        
        if st.button("Upload & Analyze") and uploaded_file is not None:
            with st.spinner("Uploading and analyzing..."):
                headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                upload_res = requests.post(f"{API_URL}/resume/upload", headers=headers, files=files)
                
                if upload_res.status_code == 200:
                    resume_id = upload_res.json().get("resume_id")
                    st.session_state["resume_id"] = resume_id
                    
                    analyze_res = requests.post(f"{API_URL}/resume/analyze/{resume_id}", headers=headers)
                    if analyze_res.status_code == 200:
                        nlp_data = analyze_res.json().get("data", {})
                        st.success("Analysis Complete!")
                        st.write(f"**Skills Detected:** {', '.join(nlp_data.get('skills', []))}")
                else:
                    st.error("Upload failed!")

        # STEP 2: JOB MATCHING (Only shows if a resume is uploaded)
        if "resume_id" in st.session_state:
            st.markdown("---")
            st.subheader("Step 2: ATS Job Matching")
            job_desc = st.text_area("Paste the Job Description here:")
            
            if st.button("Calculate ATS Score"):
                with st.spinner("Running Machine Learning Model..."):
                    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
                    payload = {"job_description": job_desc}
                    
                    match_res = requests.post(f"{API_URL}/resume/match-job/{st.session_state['resume_id']}", headers=headers, json=payload)
                    
                    if match_res.status_code == 200:
                        data = match_res.json().get("data", {})
                        
                        # Display huge metric score
                        st.metric(label="🏆 ATS Compatibility Score", value=f"{data.get('ats_score')}%")
                        
                        # Display recommendations in columns
                        col1, col2 = st.columns(2)
                        with col1:
                            st.warning("⚠️ Missing Skills")
                            for skill in data.get("missing_skills", []):
                                st.write(f"- {skill}")
                        with col2:
                            st.info("💡 AI Recommendations")
                            for rec in data.get("recommendations", []):
                                st.write(f"- {rec}")
                    else:
                        st.error("Failed to calculate score.")
    else:
        st.warning("👈 Please login via the sidebar to use the Analyzer.")

# ==========================================
# TAB 2: ADMIN ANALYTICS DASHBOARD
# ==========================================
with tab2:
    st.subheader("Platform Usage Statistics")
    
    if st.button("Refresh Analytics"):
        res = requests.get(f"{API_URL}/analytics/dashboard")
        
        if res.status_code == 200:
            data = res.json().get("data", {})
            
            # 1. Top Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Resumes Uploaded", data.get("total_resumes_uploaded", 0))
            col2.metric("Total Resumes Analyzed", data.get("total_resumes_analyzed", 0))
            col3.metric("Average ATS Score", f"{data.get('average_ats_score', 0)}%")
            
            st.markdown("---")
            
            # 2. Bar Chart for Top Skills
            top_skills = data.get("top_skills", [])
            if top_skills:
                st.write("### 🔥 Most Popular Skills Across All Users")
                # Convert the data into a Pandas DataFrame for the chart
                df = pd.DataFrame(top_skills)
                df.set_index('skill', inplace=True)
                st.bar_chart(df)
            else:
                st.info("Not enough data to display popular skills yet.")
        else:
            st.error("Failed to load dashboard data.")