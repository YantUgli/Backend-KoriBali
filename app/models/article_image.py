from app.extensions import db
from datetime import datetime, timezone

class ArticleImages(db.Model):
    __tablename__ = 'article_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    image_url = db.Column(db.String(255))

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)

    create_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))

