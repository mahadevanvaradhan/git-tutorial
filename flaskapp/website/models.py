from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
import uuid
from cryptography.fernet import Fernet
import json

# Generate and store this key securely (e.g., in environment variables)
ENCRYPTION_KEY = Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Authorization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    authorization_type = db.Column(db.String(20), nullable=False)
    values = db.Column(db.Text, nullable=False)  # Encrypted JSON

    def set_values(self, values):
        self.values = fernet.encrypt(json.dumps(values).encode()).decode()

    def get_values(self):
        return json.loads(fernet.decrypt(self.values.encode()).decode())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class APIConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    authorization_name = db.Column(db.String(100))
    method = db.Column(db.String(10), nullable=False)
    base_url = db.Column(db.String(255), nullable=False)
    url_path = db.Column(db.String(255))
    headers = db.Column(db.Text, default='{}')
    parameters = db.Column(db.Text, default='{}')
    body = db.Column(db.Text, default='{}')
    retries = db.Column(db.Integer, default=3)
    delay_response = db.Column(db.Integer, default=0)
    created_by = db.Column(db.String(100))
    

class HTTPConnector(db.Model):
    __tablename__ = 'http_connectors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    base_url = db.Column(db.String(2048), nullable=False)
    auth_type = db.Column(db.String(50), nullable=False)  # Basic, Bearer, APIKey, OAuth2
    auth_config = db.Column(db.Text, nullable=True)  # Store headers, tokens, secrets, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(50))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "base_url": self.base_url,
            "auth_type": self.auth_type,
            "auth_config": self.auth_config,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }