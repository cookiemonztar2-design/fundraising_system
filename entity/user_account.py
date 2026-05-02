from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role= db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="Active")