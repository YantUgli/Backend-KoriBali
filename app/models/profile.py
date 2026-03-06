from app.extention import db

class Profile(db.Model):

    __tablename__ = 'profiles'


    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    full_name = db.Column(db.String(150), nullable = True)
    path_image_profile = db.Column(db.String(150), nullable = True)
    address = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)