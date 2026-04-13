import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "macuin-secret-2024")
    API_URL    = os.getenv("API_URL", "http://api:8000/v1")
    DEBUG      = os.getenv("FLASK_DEBUG", "false").lower() == "true"
