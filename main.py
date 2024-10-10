# app/main.py
from fastapi import FastAPI
from auth import auth_router  # Import authentication routes

app = FastAPI()

# Include authentication routes
app.include_router(auth_router)

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI App!"}

print("hello world!")
