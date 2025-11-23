# backend/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Create extension instances here, to be initialized in server.py
db = SQLAlchemy()
jwt = JWTManager()
