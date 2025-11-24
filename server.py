# server.py
import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager

from backend import db 
from backend.routes import main

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    # --------------------
    # REQUIRED CONFIG
    # --------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # SESSION COOKIE CONFIG
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = False   # True only for HTTPS
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    # --------------------
    # INIT EXTENSIONS
    # --------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # --------------------
    # CORS (FIXED)
    # --------------------
    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": "http://localhost:5001"}},
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"]
    )
    # --------------------
    # BLUEPRINTS
    # --------------------
    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)