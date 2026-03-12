from app.extensions import db
from datetime import date
from datetime import datetime, timezone


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
