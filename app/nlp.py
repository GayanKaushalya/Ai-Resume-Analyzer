import spacy
import re
import json
import os

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Build the absolute path to our skills.json file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_FILE = os.path.join(BASE_DIR, "data", "skills.json")

# Function to load skills from the JSON file
def load_skills() -> list:
    try:
        with open(SKILLS_FILE, "r") as file:
            data = json.load(file)
            return data.get("skills", [])
    except Exception as e:
        print(f"Error loading skills.json: {e}")
        return []

# Load the skills into memory once when the app starts
SKILLS_DB = load_skills()

def extract_skills(text: str) -> list:
    """Finds skills from the text based on our SKILLS_DB."""
    text_lower = text.lower()
    
    found_skills = set()
    for skill in SKILLS_DB:
        # Check if the skill exists as a standalone word in the text
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.add(skill)
            
    return list(found_skills)

def extract_email(text: str) -> str:
    """Uses Regular Expressions (Regex) to find an email address."""
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def analyze_resume_text(text: str) -> dict:
    """Runs all NLP functions and returns a dictionary of extracted data."""
    return {
        "email": extract_email(text),
        "skills": extract_skills(text)
    }