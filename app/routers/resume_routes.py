import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.database import db
from app.auth import get_current_user

router = APIRouter(
    prefix="/resume",
    tags=["Resume API"]
)

# Create an uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".png", ".jpg", ".jpeg"}

# Connect to the resumes collection in MongoDB
resumes_collection = db["resumes"]

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...), 
    current_user_email: str = Depends(get_current_user) # This locks the route!
):
    # 1. Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}")

    # 2. Create a secure, unique filename (e.g., user@email.com_resume.pdf)
    secure_filename = f"{current_user_email}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, secure_filename)

    # 3. Save the file to our local 'uploads' folder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Save the resume data to MongoDB
    resume_data = {
        "user_email": current_user_email,
        "filename": secure_filename,
        "file_path": file_path,
        "status": "Uploaded",  # We will change this to 'Processed' in Phase 4/5
        "extracted_text": "",  # Placeholder for Phase 4
    }
    result = resumes_collection.insert_one(resume_data)

    return {
        "message": "Resume uploaded successfully!",
        "resume_id": str(result.inserted_id),
        "filename": secure_filename
    }
