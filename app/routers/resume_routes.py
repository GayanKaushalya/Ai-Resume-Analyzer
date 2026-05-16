import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.database import db
from app.auth import get_current_user
from app.utils import extract_text  # <-- IMPORT OUR NEW FUNCTION

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