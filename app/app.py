import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.secret_key = "secret-key"

    db.init_app(app)

    JWTManager(app)
    Bcrypt(app)

    # Blueprints
    from .blueprints.user.routes import user_bp

    app.register_blueprint(user_bp)

    from .blueprints.video.routes import video_bp

    app.register_blueprint(video_bp)

    # Database migrations
    Migrate(app, db)

    return app
