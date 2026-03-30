from app.extensions import db
from datetime import datetime, timezone

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable=False)
    thumbnail_path = db.Column(db.String(255))
    type = db.Column(db.Enum('rendering', 'modeling', 'drafting', 'calculating', name='project_type'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    project_images = db.relationship('ProjectImages', backref='project',  cascade='all, delete-orphan')


    def to_dict(self):
        return{
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'thumbnail_path' : self.thumbnail_path,
            'type' : self.type,
            'images' : [img.image_url for img in self.project_images],
            'created_at' : self.created_at,
            'updated_at' : self.updated_at 
        }



# PROJECT IMAGE MODEL
class ProjectImages(db.Model):
    __tablename__ = 'project_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable= False)