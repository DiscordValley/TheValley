from bot.database import db


class Profile(db.Model):
    __tablename__ = "Profile"

    user_id = db.Column(db.BIGINT, primary_key=True)
    badge_id = db.Column(db.Integer)
