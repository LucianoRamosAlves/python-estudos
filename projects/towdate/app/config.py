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

    SQLALCHEMY_TRACK_MODIFICATIONS = False