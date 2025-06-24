from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from .config import Config
from .utils.errors import register_error_handlers

jwt = JWTManager()
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})

    from app.routes import auth, users
    app.register_blueprint(auth.bp)
    app.register_blueprint(users.bp)

    with app.app_context():
        db.create_all()

    register_error_handlers(app)

    return app