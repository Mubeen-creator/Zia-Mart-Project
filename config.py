import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the MongoDB URL
MONGODB_URL = os.getenv("MONGODB_URL")

# Other configuration variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Raise an error if MONGODB_URL is not set
if not MONGODB_URL:
    raise ValueError("MONGODB_URL is not set in the .env file")

