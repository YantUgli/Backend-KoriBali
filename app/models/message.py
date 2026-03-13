from app.extensions import db
from datetime import datetime, timezone

class Message(db.Model):
    __tablename__ = "messages"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    number_phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # updated_at = db.Column(
    #     db.DateTime,
    #     default=lambda: datetime.now(timezone.utc),
    #     onupdate=lambda: datetime.now(timezone.utc)
    # )


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "number_phone": self.number_phone,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # "updated_at": self.created_at.isoformat() if self.created_at else None
        }