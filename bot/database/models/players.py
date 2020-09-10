from bot.database import db


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT)
    guild_id = db.Column(db.BIGINT)
    balance = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

    energy = db.Column(db.Integer, default=100)
    last_visit = db.Column(db.DateTime)
    allow_notification = db.Column(db.Boolean, default=False)

    _guild_user_uniq = db.UniqueConstraint("user_id", "guild_id", name="guild_user")
