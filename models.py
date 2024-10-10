# app/models.py
from pydantic import BaseModel, EmailStr

# Pydantic model for user
class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str  # Store the hashed password

class UserLoginModel(BaseModel):
    email: EmailStr  # Use email for login
    password: str  # Raw password for login validation

# Model for resetting password
class ResetPasswordModel(BaseModel):
    email: EmailStr  # Email to identify the user
    new_password: str  # New password to be set
