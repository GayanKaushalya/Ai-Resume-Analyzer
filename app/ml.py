from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_ats_score(resume_text: str, job_description: str) -> float:
    """
    Uses TF-IDF to convert text into mathematical vectors and calculates 
    the Cosine Similarity between the resume and the job description.
    """
    # Create the vectorizer, ignoring common English stop words (like "the", "and", "a")
    vectorizer = TfidfVectorizer(stop_words='english')
    
    # Convert the two texts into a matrix of numbers
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    
    # Calculate the similarity score between the first document (resume) and second (job)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Return as a percentage rounded to 2 decimal places
    return round(similarity * 100, 2)

def get_missing_skills(resume_skills: list, job_skills: list) -> list:
    """Compares the two lists and returns skills that are in the job but missing in the resume."""
    return list(set(job_skills) - set(resume_skills))