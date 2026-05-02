from entity.user_account import db

class FundRaisingActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Active")
    fundraiser_username = db.Column(db.String(100), nullable=False)