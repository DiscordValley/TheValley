from bot.database import db
from datetime import datetime


class Plant(db.Model):
    __tablename__ = "plants"

    plant_id = db.Column(db.BIGINT, primary_key=True)
    farm_id = db.Column(db.ForeignKey("farms.id"))
    crop_id = db.Column(db.BIGINT)  # Will be ForeignKey of crops.id, doesn't exist yet
    planted_at = db.Column(db.DateTime(), default=datetime.utcnow())
    coord_column = db.Column(db.Integer)
    coord_row = db.Column(db.Integer)
