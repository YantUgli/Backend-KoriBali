from app.extensions import db
from datetime import datetime, timezone

class ProjectImages(db.Model):
    __tablename__ = 'project_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable= False)