from bot.database import db
from datetime import datetime


class Plant(db.Model):
    __tablename__ = "plants"

    plant_id = db.Column(db.BIGINT, primary_key=True)
    farm_id = db.Column(db.BIGINT)
    crop_id = db.Column(db.BIGINT)
    planted_at = db.Column(db.Datetime, default=datetime.now)
    coord_column = db.Column(db.Integer)
    coord_row = db.Column(db.Integer)
