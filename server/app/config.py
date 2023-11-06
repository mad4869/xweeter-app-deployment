from os import environ, path
from dotenv import load_dotenv
import datetime

basedir = path.dirname(__file__)
load_dotenv(path.join(path.dirname(basedir), ".env"))


class Config:
    # Flask Config
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    ENVIRONMENT = environ.get("ENVIRONMENT")
    SECRET_KEY = environ.get("SECRET_KEY")

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # PostgreSQL Config
    SQLALCHEMY_DATABASE_URI = f"postgresql://{environ.get('POSTGRES_USER')}:{environ.get('POSTGRES_PASSWORD')}@{environ.get('POSTGRES_HOST')}:{environ.get('POSTGRES_PORT')}/{environ.get('POSTGRES_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_DOMAIN = "localhost"
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
