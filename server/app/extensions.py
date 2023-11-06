from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_admin import Admin
from minio import Minio
from os import environ, path
from dotenv import load_dotenv

basedir = path.dirname(__file__)
load_dotenv(path.join(path.dirname(basedir), ".env"))

# Database engine
db = SQLAlchemy()

# Database migration manager
migrate = Migrate()

# Password hash generator
bcrypt = Bcrypt()

# CORS
cors = CORS()

# User auth manager
jwt_manager = JWTManager()

# Object storage
mc = Minio(
    "localhost:9000",
    access_key=environ.get("MINIO_ACCESS_KEY"),
    secret_key=environ.get("MINIO_SECRET_KEY"),
    secure=False,
)

# Websocket
socket = SocketIO(cors_allowed_origins="*")

# Admin management
admin = Admin(name="Xweeter Admin", template_mode="bootstrap3")
