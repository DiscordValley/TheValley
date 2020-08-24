from bot.database import db


class Farm(db.Model):
    __tablename__ = "Farm"

    farm_id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT)
    name = db.Column(db.Text)
