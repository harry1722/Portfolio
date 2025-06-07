from app import db
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    Time = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(120), nullable=False)
     description = db.Column(db.String(300), nullable=False)
     file_name = db.Column(db.String(100),nullable=False)
