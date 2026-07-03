import os


class Config:
    # Flask configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "646739fd0a76c461bf6c42c8d6203805")

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///towdate.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload configuration
    # Uploads
    UPLOAD_ROOT = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "static",
        "uploads",
    )

    ALLOWED_IMAGE_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "webp",
        "gif",
    }

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # Segurança dos cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Somente em produção com HTTPS
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False  # Somente em produção com HTTPS
    REMEMBER_COOKIE_SAMESITE = "Lax"

#TODO LEMBRAR QUE SECRET_KEY E DATABASE_URL DEVEM SER DEFINIDOS EM VARIÁVEIS DE AMBIENTE EM PRODUÇÃO, NÃO NO CÓDIGO.