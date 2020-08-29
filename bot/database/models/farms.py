from bot.database import db
from bot.utils.constants import FarmSizes


class Farm(db.Model):
    __tablename__ = "farms"

    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.Text)
    size = db.Column(db.Integer, default=FarmSizes.SMALL.value)
