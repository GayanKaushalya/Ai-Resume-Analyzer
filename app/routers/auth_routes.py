from fastapi import APIRouter, HTTPException, status
from app.models import UserRegister, UserLogin, Token
from app.auth import get_password_hash, verify_password, create_access_token
from app.database import db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Connect to the 'users' collection in MongoDB
users_collection = db["users"]

@router.post("/register")
def register_user(user: UserRegister):
    # 1. Check if user already exists
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash the password
    hashed_password = get_password_hash(user.password)

    # 3. Save to MongoDB
    new_user = {
        "email": user.email,
        "password": hashed_password
    }
    users_collection.insert_one(new_user)

    return {"message": "User created successfully!"}

@router.post("/login", response_model=Token)
def login_user(user: UserLogin):
    # 1. Find the user in the database
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 2. Verify the password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # 3. Create a JWT token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}