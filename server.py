# server.py
from flask import Flask
from backend import db, jwt  # import the shared instances
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import click
from flask.cli import with_appcontext

migrate = Migrate()  # only create Migrate here

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("DB URL:", DATABASE_URL)

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///app.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import models and routes
    from backend.routes import main
    app.register_blueprint(main)

    return app  # <-- return app here

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)