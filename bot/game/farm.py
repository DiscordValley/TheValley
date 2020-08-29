from bot.database.models import Farm as FarmModel
from bot.database.models import PlantedCrop
from bot.game.crop import Crop
from bot.utils.constants import FarmSizes, FARM_SIZE
from typing import List


class Farm:
    def __init__(self, farm_id: int, size: FarmSizes, name: str):
        self.id = farm_id
        self.name = name
        self.size = size
        self.plot = self.initialize_plot()

    @classmethod
    async def load(cls, player_id: int) -> "Farm":
        farm_model = await FarmModel.query.where(
            FarmModel.player_id == player_id
        ).gino.first()
        if farm_model is None:
            farm_model = await FarmModel.create(player_id=player_id)
        farm = Farm(
            farm_id=farm_model.id, size=FarmSizes(farm_model.size), name=farm_model.name
        )
        await farm.load_crops()
        return farm

    def initialize_plot(self) -> List[List[Crop]]:
        size = FARM_SIZE.get(self.size)
        return [[None] * size.rows] * size.columns

    async def load_crops(self):
        crops = await PlantedCrop.query.where(FarmModel.id == self.id).gino.all()
        for crop in crops:
            self.place_crop(
                Crop(
                    id=crop.id,
                    farm_id=crop.farm_id,
                    crop_id=crop.crop_id,
                    planted_at=crop.planted_at,
                ),
                row=crop.coord_row,
                column=crop.coord_column,
            )

    def place_crop(self, crop: Crop, row: int, column: int):
        size = FARM_SIZE.get(self.size)
        if row >= size.rows or column >= size.columns or row < 0 or column < 0:
            raise ValueError("Crop placement out of bounds.")
        self.plot[row][column] = crop
