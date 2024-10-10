# app/auth.py
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import JWTError, jwt
from models import UserModel, UserLoginModel, ResetPasswordModel  # Import new model for password reset
from database import users_collection
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility Functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Signup API
@auth_router.post("/signup/")
async def signup(user: UserModel):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    
    await users_collection.insert_one(user_dict)
    
    return {"message": "User created successfully"}

# Login API
@auth_router.post("/login/")
async def login(user: UserLoginModel):
    existing_user = await users_collection.find_one({"email": user.email})  # Updated to use email
    if not existing_user or not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": existing_user["email"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {"access_token": access_token, "token_type": "bearer"}

# Reset Password API
@auth_router.post("/reset-password/")
async def reset_password(data: ResetPasswordModel):
    existing_user = await users_collection.find_one({"email": data.email})  # Lookup by email
    if not existing_user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    hashed_password = get_password_hash(data.new_password)  # Hash the new password
    await users_collection.update_one(
        {"email": data.email},
        {"$set": {"password": hashed_password}}  # Update the password in the database
    )
    
    return {"message": "Password reset successful"}





