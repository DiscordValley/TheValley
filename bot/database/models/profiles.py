from bot.database import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.BIGINT)
    player_id = db.Column(db.ForeignKey("players.id"))
    badge_id = db.Column(db.BIGINT)
