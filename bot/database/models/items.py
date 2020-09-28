from bot.database import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.BIGINT, primary_key=True)
    item_id = db.Column(db.BIGINT)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    cost = db.Column(db.Integer)
    creation_id = db.Column(db.Integer)