from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extention import db, jwt, migrate
from flask_cors import CORS

from app.auth.routes import auth_blueprint

def create_app():
    
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_blueprint, url_prefix = "/auth")

    return app