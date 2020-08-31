from dataclasses import dataclass
from datetime import datetime
from bot.utils.constants import PlotActions


@dataclass
class Crop:
    id: int
    farm_id: int
    crop_id: int
    planted_at: datetime
    state: int

    @classmethod
    async def new(cls, farm_id: int, crop_id: int):
        # TODO: logic for planting new crops
        pass

    async def work(self, action: PlotActions):
        # TODO: work logic for different actions, storing after work etc.
        self.state = action.value
