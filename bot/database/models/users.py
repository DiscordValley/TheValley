from bot.database import db


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.BIGINT, primary_key=True)
    balance = db.Column(db.BIGINT)
    user_xp = db.Column(db.BIGINT)
    user_level = db.Column(db.BIGINT)
    farm_id = db.Column(db.BIGINT)
    energy = db.Column(db.BIGINT)
    last_visit = db.Column(db.Date)
    allow_notif = db.Column(db.Bool)
