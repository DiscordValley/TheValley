from dataclasses import dataclass
from datetime import datetime


@dataclass
class Plant:
    id: int
    farm_id: int
    crop_id: int
    planted_at: datetime
