import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.database import db
from app.auth import get_current_user
from app.utils import extract_text  # <-- IMPORT OUR NEW FUNCTION
from app.models import JobMatchRequest  # <-- NEW
from app.ml import calculate_ats_score, get_missing_skills  # <-- NEW
from app.nlp import analyze_resume_text, extract_skills  # <-- Update this line to import extract_skills

router = APIRouter(
    prefix="/resume",
    tags=["Resume API"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".png", ".jpg", ".jpeg"}
resumes_collection = db["resumes"]

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...), 
    current_user_email: str = Depends(get_current_user)
):
    # 1. Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}")

    # 2. Create a secure filename and path
    secure_filename = f"{current_user_email}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, secure_filename)

    # 3. Save the file to our local 'uploads' folder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. EXTRACT THE TEXT using our new utility! <-- NEW
    extracted_text = extract_text(file_path, file_ext)

    # 5. Save the resume data + extracted text to MongoDB <-- UPDATED
    resume_data = {
        "user_email": current_user_email,
        "filename": secure_filename,
        "file_path": file_path,
        "status": "Processed", # Changed from "Uploaded" to "Processed"
        "extracted_text": extracted_text, 
    }
    result = resumes_collection.insert_one(resume_data)

    return {
        "message": "Resume uploaded and processed successfully!",
        "resume_id": str(result.inserted_id),
        "filename": secure_filename,
        "extracted_length": len(extracted_text) # Returns how many characters were read!
    }
@router.post("/match-job/{resume_id}")
async def match_resume_to_job(
    resume_id: str, 
    request: JobMatchRequest,
    current_user_email: str = Depends(get_current_user)
):
    # 1. Find the resume in MongoDB
    try:
        resume = resumes_collection.find_one({
            "_id": ObjectId(resume_id), 
            "user_email": current_user_email
        })
    except:
        raise HTTPException(status_code=400, detail="Invalid Resume ID format")

    if not resume or "extracted_text" not in resume or "nlp_data" not in resume:
        raise HTTPException(
            status_code=400, 
            detail="Resume not found or hasn't been analyzed yet. Please call /analyze first."
        )

    resume_text = resume["extracted_text"]
    resume_skills = resume["nlp_data"].get("skills", [])

    # 2. Extract skills from the Job Description using our NLP brain
    job_skills = extract_skills(request.job_description)

    # 3. Calculate missing skills
    missing_skills = get_missing_skills(resume_skills, job_skills)

    # 4. Calculate the overall ATS Similarity Score using Scikit-Learn
    ats_score = calculate_ats_score(resume_text, request.job_description)

    # 5. Formulate recommendations
    recommendations = []
    if ats_score < 50:
        recommendations.append("Your resume similarity is low. Try adding more keywords from the job description.")
    if missing_skills:
        recommendations.append(f"Consider adding these missing skills: {', '.join(missing_skills)}")

    match_results = {
        "ats_score": ats_score,
        "job_skills_detected": job_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }

    # 6. Save the match history to MongoDB (Optional but great for history tracking!)
    resumes_collection.update_one(
        {"_id": ObjectId(resume_id)},
        {"$push": {"match_history": match_results}} # $push adds it to a list in Mongo
    )

    return {
        "message": "ATS Scoring complete!",
        "data": match_results
    }