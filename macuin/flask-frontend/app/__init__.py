# flask-frontend/app/__init__.py
from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "macuin-secret-2024")

    from .routes import main
    app.register_blueprint(main)

    return app
