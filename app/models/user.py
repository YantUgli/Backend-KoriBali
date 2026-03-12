import enum
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


# ada dua cara mendefinisikan sebuah enum
# Cara 1
class UserRole(enum.Enum):
    MEMBER = 'member'
    USER = 'user'
    
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    number_phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    # Cara 1
    # role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)

    # Cara 2
    role = db.Column(db.Enum('member', 'user', name='user_roles'), default='user', nullable=False)

    # List relation, untuk yang didalam kutip itu nama class
    profiles = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    employee_details = db.relationship('EmployeeDetail', backref='user', uselist=False, cascade='all, delete-orphan')


    # Fungsi untuk hash dan check password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)