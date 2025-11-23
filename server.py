# server.py
import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

from backend import db, jwt  # shared instances
from backend.routes import main

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")

migrate = Migrate()  # Create migrate instance

def create_app():
    app = Flask(__name__)

    # --------------------
    # REQUIRED CONFIG
    # --------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

    # --------------------
    # INIT EXTENSIONS
    # --------------------
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # --------------------
    # CORS
    # --------------------
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5001"}})

    # --------------------
    # BLUEPRINTS
    # --------------------
    app.register_blueprint(main)

    return app


# ----------------- Run Server -----------------
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)