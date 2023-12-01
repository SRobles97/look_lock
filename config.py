# config.py
import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS').split(',')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:" \
                              f"{os.getenv('DB_PASSWORD')}@" \
                              f"{os.getenv('DB_HOST')}:" \
                              f"{os.getenv('DB_PORT')}/" \
                              f"{os.getenv('DB_NAME')}"
