from fastapi import FastAPI
from app.database import db
from app.routers import auth_routes  # <-- Import the new routes
from app.routers import resume_routes 
from app.routers import analytics_routes

app = FastAPI(
    title="AI Resume Analyzer API",
    description="Backend API for ATS Scoring and Resume Analysis using MongoDB",
    version="1.0.0"
)

# Include the auth routes
app.include_router(auth_routes.router)  # <-- Connect the routes to the app
app.include_router(resume_routes.router) # <-- Connect the routes to the app
app.include_router(analytics_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Resume Analyzer API!"}

@app.get("/health")
def health_check():
    try:
        db.command('ping')
        return {"status": "Database connection is active and API is running!"}
    except Exception as e:
        return {"status": "API is running, but database connection failed.", "error": str(e)}