from bot.database import db


class Inventory(db.Model):
    __tablename__ = "inventories"

    id = db.Column(db.BIGINT, primary_key=True)
    player_id = db.Column(db.ForeignKey("players.id"))
    item_id = db.Column(db.BIGINT)  # Will be ForeignKey of item.id, doesn't exist yet
    quantity = db.Column(db.Integer)
