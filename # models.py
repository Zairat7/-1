# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Review(db.Model):
    """Класс 1: SQLAlchemy-модель для хранения отзывов"""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product,
            "text": self.text,
            "rating": self.rating,
            "date": self.date.strftime("%Y-%m-%d")
        }
