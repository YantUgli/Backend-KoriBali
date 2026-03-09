from app.extensions import db
from datetime import date

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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
