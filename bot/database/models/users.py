from bot.database import db


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.BIGINT, primary_key=True)
    balance = db.Column(db.BIGINT)
    user_xp = db.Column(db.Integer)
    user_level = db.Column(db.Integer)
    farm_id = db.Column(db.BIGINT)
    energy = db.Column(db.Integer)
    last_visit = db.Column(db.DateTime)
    allow_notif = db.Column(db.Bool)
