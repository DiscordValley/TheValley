from bot.database import db


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT)
    guild_id = db.Column(db.BIGINT)
    farm_id = db.Column(db.ForeignKey("farms.id"))
    balance = db.Column(db.Integer)
    user_xp = db.Column(db.Integer)
    user_level = db.Column(db.Integer)

    energy = db.Column(db.Integer)
    last_visit = db.Column(db.DateTime)
    allow_notification = db.Column(db.Boolean)

    _guild_user_uniq = db.UniqueConstraint("user_id", "guild_id", name="guild_user")
