# backend/__init__.py
# Can be empty or contain shared extensions if you prefer

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()