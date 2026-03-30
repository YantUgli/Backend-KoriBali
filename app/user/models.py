import enum
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, date


# ada dua cara mendefinisikan sebuah enum
# Cara 1
class UserRole(enum.Enum):
    MEMBER = 'member'
    USER = 'user'
    
# USER MODEL
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    number_phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(
            db.Enum("user", "admin", name="user_roles"),
            default="user",
            nullable=False
        )
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



# PROFILE MODEL
class Profile(db.Model):

    __tablename__ = 'profiles'


    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    full_name = db.Column(db.String(150), nullable = True)
    path_image_profile = db.Column(db.String(150), nullable = True)
    address = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



# EMPLOYEE DETAIL MODEL
class EmployeeDetail(db.Model):
    __tablename__ = "employee_details"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    division = db.Column(db.Enum('ys', 'yp', 'dev', name='division_name'), nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    joined_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
