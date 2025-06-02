import os
from dotenv import load_dotenv


load_dotenv() #nga ketu marrim variablat e .env file

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-if-not-set')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER =  os.getenv('UPLOAD_FOLDER','static/uploads')
