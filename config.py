import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")

    DATABASE = os.path.join("instance", "database.db")
    UPLOAD_FOLDER = os.path.join("static", "uploads")

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")