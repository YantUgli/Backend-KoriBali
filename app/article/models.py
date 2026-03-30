from app.extensions import db
from datetime import datetime, timezone

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    thumbnail_path = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc)
    )

    author = db.relationship('User', backref='articles')

    article_images = db.relationship('ArticleImages', backref='article', cascade='all, delete-orphan')

    def to_dict(self):
        return{
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'thumbnail_path' : #self.thumbnail_path, 
            {'medium': self.thumbnail_path},
            'user_id' : self.user_id,
            'author_name' : self.author.username,

            'images' : [
                    # {'url' : img.image_url}
                    {
                        'original' : img.original_url,
                        'medium' : img.medium_url,
                        'thumbnail': img.thumbnail_url
                    }
                for img in self.article_images
            ],
            # image di panggil dengan format 
            # "images": [
            # {
            #     "url": "uploads/a4b2185b-4a91-4d12-b137-65a42a22f6b1.jpg"
            # },
            # {
            #     "url": "uploads/9c8971c1-80e1-40e5-9df9-b7ce09953ce5.jpeg"
            # }]
            
            # lebih semantic saat pemanggilan di frontend
            # images.map(img => (
            #     <img src={img.url} />
            # ))


            #  self.published_at.isoformat() if self.published_at else None
            'created_at' : self.created_at,
            'update_at' : self.updated_at
        }
    


# ARTICLE IMAGE MODEL
class ArticleImages(db.Model):
    __tablename__ = 'article_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    # image_url = db.Column(db.String(255))

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    original_url = db.Column(db.String(255))
    medium_url = db.Column(db.String(255))
    thumbnail_url = db.Column(db.String(255))

    create_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc))

