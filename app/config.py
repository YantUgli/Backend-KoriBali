import os
from datetime import timedelta

class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:p0099@localhost/koribali_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret-key-backup-kalau-tidak-ada-di-env")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)