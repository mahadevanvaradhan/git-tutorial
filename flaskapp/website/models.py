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
    method = db.Column(db.String(10), nullable=False)
    base_url = db.Column(db.String(255), nullable=False)
    url_path = db.Column(db.String(255))
    headers = db.Column(db.Text, default='{}')
    parameters = db.Column(db.Text, default='{}')
    body = db.Column(db.Text, default='{}')
    retries = db.Column(db.Integer, default=3)
    delay_response = db.Column(db.Integer, default=0)
    created_by = db.Column(db.String(50))
    auth_type = db.Column(db.String(20), default='none')
    basic_username = db.Column(db.String(100))
    basic_password = db.Column(db.String(100))
    bearer_token = db.Column(db.String(255))
    api_key = db.Column(db.String(255))
    api_key_value = db.Column(db.String(100))