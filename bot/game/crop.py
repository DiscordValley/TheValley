from dataclasses import dataclass
from datetime import datetime


@dataclass
class Crop:
    id: int
    farm_id: int
    crop_id: int
    planted_at: datetime
