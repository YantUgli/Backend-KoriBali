from flask import Flask, send_from_directory, current_app
from dotenv import load_dotenv
from .config import Config
from .extensions import db, jwt, migrate
from flask_cors import CORS
import os

from app.auth.routes import auth_blueprint
from app.user.routes import user_blueprint
from app.message.routes import message_blueprint
from app.project.routes import project_blueprint
from app.article.routes import article_blueprint
from app.report.routes import report_blueprint

def create_app():
    
    load_dotenv()

    app = Flask(
        __name__,
        static_folder="../uploads",
        static_url_path="/uploads"
        )
    app.config.from_object(Config)


    # @app.route('/uploads/profile/<filename>')
    # def get_profile_image(filename):
    #     upload_folder = os.path.join(current_app.root_path, "...", "uploads", "profile")
    #     return send_from_directory(upload_folder, filename)

    
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        
        identity = jwt_data["sub"]
        return User.query.get(identity)
    
    # LIST MODEL
    from app.user.models import User, Profile, EmployeeDetail
    from app.article.models import Article, ArticleImages
    from app.project.models import Project, ProjectImages
    from app.message.models import Message

    # LIST ROUTE
    app.register_blueprint(auth_blueprint, url_prefix = "/auth")
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(message_blueprint, url_prefix='/message')
    app.register_blueprint(project_blueprint, url_prefix = '/project')
    app.register_blueprint(article_blueprint, url_prefix='/article')
    app.register_blueprint(report_blueprint, url_prefix='/report')

    return app