from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .extensions import db, jwt, migrate
from flask_cors import CORS
from app.models.user import User

from app.auth.routes import auth_blueprint
from app.user.routes import user_blueprint
from app.message.routes import message_blueprint

def create_app():
    
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        
        identity = jwt_data["sub"]
        return User.query.get(identity)

    app.register_blueprint(auth_blueprint, url_prefix = "/auth")
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(message_blueprint, url_prefix='/message')

    return app