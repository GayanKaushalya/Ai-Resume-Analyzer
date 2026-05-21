from fastapi import APIRouter, Depends
from app.database import db
from collections import Counter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics Dashboard"]
)

@router.get("/dashboard")
async def get_dashboard_stats():
    # 1. Fetch all resumes from MongoDB
    resumes = list(db["resumes"].find({}))
    
    total_resumes = len(resumes)
    analyzed_resumes = 0
    all_skills = []
    ats_scores = []

    # 2. Loop through the data to calculate statistics
    for resume in resumes:
        if resume.get("status") == "Analyzed" or "nlp_data" in resume:
            analyzed_resumes += 1
            # Collect all skills for the popular skills chart
            skills = resume.get("nlp_data", {}).get("skills", [])
            all_skills.extend(skills)
            
        # Collect ATS scores if they have been matched to a job
        match_history = resume.get("match_history", [])
        if match_history:
            # Get the most recent match score
            latest_score = match_history[-1].get("ats_score", 0)
            ats_scores.append(latest_score)

    # 3. Calculate Top 5 most popular skills
    skill_counts = Counter(all_skills)
    top_skills = [{"skill": skill, "count": count} for skill, count in skill_counts.most_common(5)]

    # 4. Calculate Average ATS Score
    avg_score = sum(ats_scores) / len(ats_scores) if ats_scores else 0

    return {
        "message": "Analytics retrieved successfully",
        "data": {
            "total_resumes_uploaded": total_resumes,
            "total_resumes_analyzed": analyzed_resumes,
            "average_ats_score": round(avg_score, 2),
            "top_skills": top_skills
        }
    }