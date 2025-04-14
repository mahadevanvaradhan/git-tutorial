from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import uuid


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class APIConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    method = db.Column(db.String(10), nullable=False)
    base_url = db.Column(db.String(200), nullable=False)
    url_path = db.Column(db.String(200), nullable=False)
    parameters = db.Column(db.JSON, nullable=True)
    body = db.Column(db.JSON, nullable=True)
    retries = db.Column(db.Integer, default=3)
    delay_response = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)