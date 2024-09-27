import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PostgreSQL database URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Use a secure secret key for sessions
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")