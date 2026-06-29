import os

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "646739fd0a76c461bf6c42c8d6203805"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///towdate.db"
    )

    UPLOAD_FOLDER = "app/static/uploads/profile_pictures"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Segurança dos cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False     # Somente em produção com HTTPS
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False     # Somente em produção com HTTPS
    REMEMBER_COOKIE_SAMESITE = "Lax"