from bot.database import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    cost = db.Column(db.Integer)
    creation_id = db.Column(db.BIGINT)
