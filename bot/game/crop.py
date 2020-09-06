from dataclasses import dataclass
from datetime import datetime
from bot.utils.constants import PlotActions
from bot.database.models import PlantedCrop


@dataclass
class Crop:
    id: int
    farm_id: int
    crop_id: int
    planted_at: datetime
    state: int

    @classmethod
    async def new(cls, farm_id: int, crop_id: int, row: int, column: int):
        crop = await PlantedCrop.create(
            farm_id=farm_id, crop_id=crop_id, coord_column=column, coord_row=row
        )
        return Crop(crop.id, crop.farm_id, crop.crop_id, crop.planted_at, crop.state)

    async def work(self, action: PlotActions):
        # TODO: work logic for different actions, storing after work etc.
        self.state = action.value
