from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

CATEGORIES = ['Groceries', 'Leisure', 'Electronics', 'Utilities', 'Clothing', 'Health', 'Others']

class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at    = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expenses      = db.relationship('Expense', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id':    self.id,
            'name':  self.name,
            'email': self.email,
        }


class Expense(db.Model):
    __tablename__ = 'expenses'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    amount      = db.Column(db.Numeric(10, 2), nullable=False)  # float stores numbers in binary and loses precision (0.1 + 0.2 = 0.30000000000000004)
                                                                # unacceptable for money, Numeric stores exact decimal
    date        = db.Column(db.Date, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id':       self.id,
            'title':    self.title,
            'amount':   float(self.amount),  # Numeric is a Python object, not JSON-serializable — convert to float only for the response, precision stays intact in DB
            'category': self.category,
            'date':     self.date.isoformat(), # date is a Python object, not JSON-serializable — .isoformat() converts it to string '2026-03-15' only for the response
        }